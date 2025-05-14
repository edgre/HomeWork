import { useState } from "react";

import RatingInput from "./ratePanel";

import "../../assets/styles/font.css";
import "../../assets/styles/buttons.css";
import "../../assets/styles/colors.css";
import "../../assets/styles/text.css";
import "../../assets/styles/authPage.css";
import "../../assets/styles/photo.css";
import defaultPhoto from "../../assets/images/image 6110.png";

const PreviewHomework = ({
  taskTextFull,
  photoUrl = defaultPhoto,
  altText = "Фотография",
}) => {
  const [userRating, setUserRating] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(false);
  const handleRatingChange = (newRating) => {
    console.log("Новый рейтинг:", newRating);
    setUserRating(newRating);
    // Здесь можно добавить вызов API для сохранения в БД
  };
  const handleImageLoad = () => {
    setIsLoading(false);
  };

  const handleImageError = () => {
    setError(true);
    setIsLoading(false);
  };
  return (
    <div className="auth-form-container">
      <h2 className="bold">Задача</h2>
      <h4>{taskTextFull}</h4>
      <h2 className="bold">Решение</h2>
      <div className="photo-container">
        {isLoading && <div className="photo-loader">Загрузка...</div>}
        {error ? (
          <div className="photo-error">Ошибка загрузки</div>
        ) : (
          <img
            src={photoUrl}
            alt={altText}
            className="photo-image"
            onLoad={handleImageLoad}
            onError={handleImageError}
          />
        )}
      </div>
      <h2 className="bold">Ответ</h2>
      <h4>Какой-то ответ</h4>
      <RatingInput
        label="Оцените работу пользователя"
        onRatingChange={handleRatingChange}
      />
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginTop: "16px",
        }}
        onClick={() => setModalActive(false)}
      >
        <button type="submit" className="button">
          ОК
        </button>
      </div>
    </div>
  );
};

export default PreviewHomework;
