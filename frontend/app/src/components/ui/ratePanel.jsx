import React, { useState } from "react";
import StarEmpty from "../../assets/images/StarEmpty.svg";
import StarFilled from "../../assets/images/Star.svg";
import "../../assets/styles/rating.css";

const RatingInput = ({
  label = "Оцените пользователя:",
  onRatingChange = (rating) => {},
}) => {
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);

  const handleClick = (selectedRating) => {
    setRating(selectedRating);
    onRatingChange(selectedRating);
  };

  return (
    <div className="rating-container">
      <h4>{label}</h4>
      <div className="stars-container">
        {[1, 2, 3, 4, 5].map((star) => (
          <img
            key={star}
            src={star <= (hoverRating || rating) ? StarFilled : StarEmpty}
            alt={star}
            style={{
              width: "24px",
              height: "24px",
              cursor: "pointer",
              filter:
                star <= (hoverRating || rating)
                  ? "none"
                  : "opacity(0.7) grayscale(100%)",
              transition: "filter 0.2s ease",
            }}
            onMouseEnter={() => setHoverRating(star)}
            onMouseLeave={() => setHoverRating(0)}
            onClick={() => handleClick(star)}
          />
        ))}
      </div>
    </div>
  );
};

export default RatingInput;
