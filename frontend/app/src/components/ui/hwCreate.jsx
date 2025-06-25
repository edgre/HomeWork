import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../../contexts/UserContext";
import "../../assets/styles/font.css";
import "../../assets/styles/buttons.css";
import "../../assets/styles/colors.css";
import "../../assets/styles/text.css";
import "../../assets/styles/authPage.css";

import FileUploadButton from "./fileUpload";
import DropdownList from "./dropdownList";

const HomeworkCreate = () => {
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedSubcategory, setSelectedSubcategory] = useState("");
  const [shortDescription, setShortDescription] = useState("");
  const [fullDescription, setFullDescription] = useState("");
  const [price, setPrice] = useState("");
  const [shortAnswer, setShortAnswer] = useState("");
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isElite, setIsElite] = useState(false);
  const [userRating, setUserRating] = useState(0);

  const navigate = useNavigate();
  const { user, updateUser } = useContext(UserContext);

  useEffect(() => {
    const fetchUserRating = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) {
        setError("Токен авторизации не найден");
        return;
      }

      try {
        const response = await fetch("/api/users/me", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Ошибка при получении профиля");
        }

        const userData = await response.json();
        setUserRating(userData.user_rating || 0);
      } catch (err) {
        setError(err.message || "Ошибка при получении рейтинга");
      }
    };

    const fetchDraft = async () => {
      const token = localStorage.getItem("access_token");
      if (!token || !user?.has_draft) {
        return;
      }

      try {
        const response = await fetch("/api/gdz/get_draft", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Ошибка при получении черновика");
        }

        const draftData = await response.json();
        if (draftData.category) setSelectedCategory(draftData.category);
        if (draftData.subject) setSelectedSubcategory(draftData.subject);
        if (draftData.description) setShortDescription(draftData.description);
        if (draftData.full_description) setFullDescription(draftData.full_description);
        if (draftData.price !== undefined && draftData.price !== null) setPrice(draftData.price.toString());
        if (draftData.content_text) setShortAnswer(draftData.content_text);
        if (draftData.is_elite !== undefined) setIsElite(draftData.is_elite);
      } catch (err) {
        setError(err.message || "Ошибка при получении черновика");
      }
    };

    fetchUserRating();
    fetchDraft();
  }, [user]);

  const validateInput = (input) => {
    if (typeof input === "string" && (input.includes("{{") || input.includes("{%"))) {
      throw new Error("Недопустимые символы в вводе");
    }
    return input;
  };

  const saveDraftToServer = async () => {
    console.log("saveDraftToServer вызвана");
    // Проверяем, есть ли данные для сохранения
    const shouldSave = selectedCategory || selectedSubcategory || shortDescription || fullDescription || price || shortAnswer || isElite;
    if (!shouldSave) {
      console.log("Нет данных для сохранения черновика");
      return;
    }

    const token = localStorage.getItem("access_token");
    if (!token) {
      setError("Токен авторизации отсутствует");
      return;
    }

    try {
      const draftData = {
        category: validateInput(selectedCategory) || "",
        subject: validateInput(selectedSubcategory) || "",
        description: validateInput(shortDescription) || "",
        full_description: validateInput(fullDescription) || "",
        content_text: validateInput(shortAnswer) || "",
        price: parseInt(price) || 0,
        is_elite: isElite,
        gdz_id: null,
      };

      const response = await fetch("/api/gdz/save_draft", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json", // Указываем JSON
        },
        body: JSON.stringify(draftData), // Отправляем данные как JSON
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({
          detail: `HTTP ${response.status}: Ошибка сервера`,
        }));
        throw new Error(errorData.detail || `Не удалось сохранить черновик: Ошибка ${response.status}`);
      }

      const responseData = await response.json();
      console.log("Черновик успешно сохранен:", responseData);
      updateUser({ has_draft: true });
    } catch (err) {
      setError(err.message || "Не удалось сохранить черновик. Пожалуйста, попробуйте снова.");
      console.error("Ошибка в saveDraftToServer:", err);
    }
  };

  const handleBackClick = async (e) => {
    e.preventDefault();
    await saveDraftToServer();
    navigate("/home");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    if (!selectedCategory || !selectedSubcategory) {
      setError("Пожалуйста, выберите категорию и предмет");
      setIsLoading(false);
      return;
    }

    try {
      const formData = new FormData();
      if (file) {
        formData.append("content_file", file);
      }
      const combinedCategory = `${validateInput(selectedCategory)}_${validateInput(selectedSubcategory)}`;
      const gdzData = {
        category: combinedCategory,
        description: validateInput(shortDescription),
        full_description: validateInput(fullDescription),
        price: parseInt(price) || 0,
        content_text: validateInput(shortAnswer),
        is_elite: isElite,
      };
      formData.append("gdz_str", JSON.stringify(gdzData));

      const response = await fetch("/api/gdz/create", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({
          detail: `HTTP ${response.status}: Ошибка сервера`,
        }));
        throw new Error(errorData.detail || `Не удалось опубликовать ГДЗ: Ошибка ${response.status}`);
      }

      const responseData = await response.json();
      alert("ГДЗ успешно опубликовано!");
      console.log("Публикация завершена, сброс формы:", responseData);

      setSelectedCategory("");
      setSelectedSubcategory("");
      setShortDescription("");
      setFullDescription("");
      setPrice("");
      setShortAnswer("");
      setFile(null);
      setIsElite(false);
      updateUser({ has_draft: false });
      navigate("/home");
    } catch (err) {
      setError(err.message || "Не удалось опубликовать ГДЗ. Пожалуйста, попробуйте снова.");
      console.error("Ошибка в handleSubmit:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-form-container" style={{ marginTop: "42px", position: "relative" }}>
      <button className="back-button" onClick={handleBackClick}>
        ←
      </button>
      <h1 className="h1" style={{ verticalAlign: "center", justifyContent: "center" }}>
        Создание своего ГДЗ
      </h1>
      {error && (
        <div className="error-message" style={{ color: "red", marginBottom: "16px" }}>
          {error}
        </div>
      )}
      <form className="auth-form" onSubmit={handleSubmit}>
        <DropdownList
          onCategoryChange={setSelectedCategory}
          onSubcategoryChange={setSelectedSubcategory}
          initialCategory={selectedCategory}
          initialSubcategory={selectedSubcategory}
        />
        <div className="form-group">
          <h4 style={{ color: "#000", marginBottom: "8px" }}>
            Краткое описание задания
          </h4>
          <input
            type="text"
            className="inputBox"
            placeholder="Кратко опишите задание"
            value={shortDescription}
            onChange={(e) => setShortDescription(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <h4 style={{ color: "#000", marginBottom: "8px" }}>
            Полная формулировка задания
          </h4>
          <textarea
            className="inputBox"
            placeholder="Подробное описание задания"
            value={fullDescription}
            onChange={(e) => setFullDescription(e.target.value)}
            required
            rows={4}
          />
        </div>
        <div className="form-group">
          <h4 style={{ color: "#000" }}>Цена</h4>
          <h4 style={{ marginBottom: "8px" }}>(Числом, 0 = бесплатно)</h4>
          <input
            type="number"
            className="inputBox"
            placeholder="0"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            min="0"
            step="0.01"
            required
          />
        </div>
        <div className="form-group">
          <h4 style={{ color: "#000", marginBottom: "8px" }}>Короткий ответ</h4>
          <input
            type="text"
            className="inputBox"
            placeholder="Основной ответ на задание"
            value={shortAnswer}
            onChange={(e) => setShortAnswer(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <h4 style={{ color: "#000", marginBottom: "8px" }}>
            Загрузить решение (PDF, Word, изображения)
          </h4>
          <FileUploadButton onFileSelect={setFile} />
          {file && (
            <div style={{ marginTop: "8px", fontSize: "14px" }}>
              Выбран файл: {file.name}
            </div>
          )}
        </div>
        {userRating >= 4.8 && (
          <div className="form-group" style={{ display: "flex", alignItems: "center" }}>
            <input
              type="checkbox"
              id="isElite"
              checked={isElite}
              onChange={(e) => setIsElite(e.target.checked)}
              style={{ marginRight: "8px" }}
            />
            <label htmlFor="isElite" style={{ color: "#000" }}>
              Сделать элитным ГДЗ
            </label>
          </div>
        )}
        <div className="form-group">
          <button
            type="submit"
            className="button"
            style={{ marginTop: "8px" }}
            disabled={isLoading}
          >
            {isLoading ? "Отправка..." : "Опубликовать"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default HomeworkCreate;