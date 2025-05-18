import { useState } from "react";
import "../../assets/styles/font.css";
import "../../assets/styles/buttons.css";
import "../../assets/styles/colors.css";
import "../../assets/styles/text.css";
import "../../assets/styles/authPage.css";

import FileUploadButton from "./fileUpload";
import DropdownList from "./dropdownList";

const HomeworkCreate = () => {
  // Состояния для формы
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedSubcategory, setSelectedSubcategory] = useState("");
  const [shortDescription, setShortDescription] = useState("");
  const [fullDescription, setFullDescription] = useState("");
  const [price, setPrice] = useState("");
  const [shortAnswer, setShortAnswer] = useState("");
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Обработчик отправки формы
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    // Валидация
    if (!selectedCategory || !selectedSubcategory) {
      setError("Пожалуйста, выберите категорию и предмет");
      setIsLoading(false);
      return;
    }

    try {
      const formData = new FormData();

      // Добавляем файл, если он есть
      if (file) {
        formData.append("content_file", file);
      }

      const combinedCategory = `${selectedCategory}_${selectedSubcategory}`;

      // Создаем объект с данными GDZ
      const gdzData = {
        category: combinedCategory,
        description: shortDescription,
        full_description: fullDescription,
        price: parseInt(price),
        content_text: shortAnswer,
      };

      formData.append("gdz_str", JSON.stringify(gdzData));

      // Отправка данных на сервер
      const response = await fetch("api/gdz/create", {
        method: "POST",
        body: formData,
        headers: {
          "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Ошибка при создании ГДЗ");
      }

      // Обработка успешного ответа
      const result = await response.json();
      console.log("ГДЗ успешно создано:", result);
      alert("ГДЗ успешно опубликовано!");
      // Здесь можно добавить редирект: navigate('/success');

    } catch (err) {
      setError(err.message || "Произошла ошибка при отправке данных");
      console.error("Ошибка:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-form-container" style={{ marginTop: "42px" }}>
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