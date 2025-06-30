import React, { useState, useRef, useEffect } from "react";
import "../../assets/styles/text.css";

const TooltipText = ({ text, maxLength, as: Tag = "span" }) => {
  // Добавляем параметр `as`
  const [isVisible, setIsVisible] = useState(false);

  const truncatedText =
    text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;

  const tooltipRef = useRef(null);

  useEffect(() => {
    if (isVisible && tooltipRef.current) {
      const rect = tooltipRef.current.getBoundingClientRect();
      if (rect.right > window.innerWidth) {
        tooltipRef.current.style.left = "auto";
        tooltipRef.current.style.right = "0";
      }
    }
  }, [isVisible]);

  return (
    <Tag // Используем переданный тег (по умолчанию 'span')
      className="truncated-text"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      aria-label={text}
    >
      {truncatedText}
      {isVisible && text.length > maxLength && (
        <div className="custom-tooltip">{text}</div>
      )}
    </Tag>
  );
};

export default TooltipText;
