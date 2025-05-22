import { useState } from "react";
import "../../assets/styles/font.css";
import "../../assets/styles/buttons.css";
import "../../assets/styles/colors.css";
import "../../assets/styles/text.css";
import "../../assets/styles/authPage.css";

const PaymentForm = ({ nonce, gdzId, onClose, onSuccess }) => {
  const [cardNumber, setCardNumber] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    setSuccess(null);

    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Вы не авторизованы. Пожалуйста, войдите в систему.");
      }

      const response = await fetch(`/api/gdz/${gdzId}/confirm-purchase`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          value: cardNumber,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка при обработке платежа");
      }

      const data = await response.json();
      setSuccess("Платеж успешно обработан!");
      setCardNumber("");

      // Вызываем onSuccess для отображения ГДЗ
      if (onSuccess) {
        onSuccess();
      }

      // Закрываем форму через 2 секунды, если передан onClose
      // if (onClose) {
      //     setTimeout(() => onClose(), 2000);
      // }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="auth-form-container">
      <h1
        className="h1"
        style={{ verticalAlign: "center", justifyContent: "center" }}
      >
        Оплата
      </h1>
      <h2
        style={{
          marginTop: "5px",
          marginBottom: "16px",
          verticalAlign: "center",
          justifyContent: "center",
        }}
      >
        Введите данные вашей карты
      </h2>

      <h2 style={{ marginBottom: "16px" }}>Сеанс: {nonce}</h2>

      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            type="text"
            id="cardNumber"
            className="inputBox"
            placeholder="Номер карты"
            value={cardNumber}
            onChange={(e) => setCardNumber(e.target.value)}
            required
            disabled={isSubmitting}
          />
        </div>

        {error && (
          <p className="error-text" style={{ color: "red", margin: "10px 0" }}>
            {error}
          </p>
        )}
        {success && (
          <p
            className="success-text"
            style={{ color: "green", margin: "10px 0" }}
          >
            {success}
          </p>
        )}

        <div className="form-group">
          <button
            type="submit"
            className="button"
            style={{ marginTop: "8px" }}
            disabled={isSubmitting || !cardNumber}
          >
            {isSubmitting ? "Обработка..." : "Оплатить"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PaymentForm;
