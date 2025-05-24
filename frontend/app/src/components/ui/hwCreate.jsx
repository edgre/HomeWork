import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
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

  const navigate = useNavigate();

  useEffect(() => {
    const fetchDraft = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) {
        setError("Токен авторизации не найден");
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
          if (response.status === 404) {
            return;
          }
          const errorData = await response.json();
          throw new Error(errorData.detail || "Ошибка при получении черновика");
        }

        const draftData = await response.json();

        // Populate form fields with non-empty draft data
        if (draftData.category) setSelectedCategory(draftData.category);
        if (draftData.subject) setSelectedSubcategory(draftData.subject);
        if (draftData.description) setShortDescription(draftData.description);
        if (draftData.full_description) setFullDescription(draftData.full_description);
        if (draftData.price !== undefined && draftData.price !== null) setPrice(draftData.price.toString());
        if (draftData.content_text) setShortAnswer(draftData.content_text);
        // Note: File is not populated as it requires special handling (e.g., fetching the file from a URL or path)
      } catch (err) {
        setError(err.message || "Ошибка при получении черновика");
      }
    };

    fetchDraft();
  }, []); // Empty dependency array to run once on mount

  const saveDraftToServer = async () => {
    const shouldSave = selectedCategory || selectedSubcategory || shortDescription || fullDescription || price || shortAnswer || file;
    if (!shouldSave) {
      return;
    }

    const token = localStorage.getItem("access_token");
    if (!token) {
      return;
    }

    const formData = new FormData();
    const draftData = {
      category: selectedCategory,
      subject: selectedSubcategory,
      description: shortDescription,
      full_description: fullDescription,
      content_text: shortAnswer,
      price: parseInt(price) || 0,
      is_elite: false,
    };
    formData.append("gdz_str", JSON.stringify(draftData));
    if (file) {
      formData.append("file", file);
    }

    try {
      const response = await fetch("/api/gdz/save_draft", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Ошибка при сохранении черновика");
      }

      await response.json();
    } catch (err) {
      setError(err.message || "Ошибка при сохранении черновика");
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

    // Validation
    if (!selectedCategory || !selectedSubcategory) {
      setError("Пожалуйста, выберите категорию и предмет");
      setIsLoading(false);
      return;
    }

    // Save draft before submitting
    await saveDraftToServer();

    try {
      const formData = new FormData();

      // Add file if it exists
      if (file) {
        formData.append("content_file", file);
      }

      const combinedCategory = `${selectedCategory}_${selectedSubcategory}`;

      // Create GDZ data object
      const gdzData = {
        category: combinedCategory,
        description: shortDescription,
        full_description: fullDescription,
        price: parseInt(price),
        content_text: shortAnswer,
      };

      formData.append("gdz_str", JSON.stringify(gdzData));

      // Send data to server
      const response = await fetch("/api/gdz/create", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Ошибка при создании ГДЗ");
      }

      // Handle successful response
      await response.json();
      alert("ГДЗ успешно опубликовано!");
    } catch (err) {
      setError(err.message || "Произошла ошибка при отправке данных");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-form-container" style={{ marginTop: "42px", position: "relative" }}>
      {/* Back button */}
      <a href="/home" className="back-button" onClick={handleBackClick}>
        ←
      </a>

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