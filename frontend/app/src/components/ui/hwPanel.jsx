import { useState, useEffect, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { UserContext } from "../../contexts/UserContext";
import TooltipText from "./tooltipText";
import Modal from "./modal";
import PaymentForm from "./paymentForm";
import PreviewHomework from "./previewHomework";
import "../../assets/styles/headers.css";
import "../../assets/styles/grid.css";
import "../../assets/styles/text.css";

const HomeWorkPanel = ({ number, taskText, price, ownerId, has_purchased }) => {
  const [modalActive, setModalActive] = useState(false);
  const [nonce, setNonce] = useState(null);
  const [error, setError] = useState(null);
  const [showGdz, setShowGdz] = useState(false);
  const [isOwner, setIsOwner] = useState(false);
  const { slug } = useParams();
  const navigate = useNavigate();
  const { user } = useContext(UserContext);
  const token = localStorage.getItem("access_token");

  // Проверка, является ли пользователь владельцем ГДЗ
  useEffect(() => {
    if (user?.id && ownerId === user.id) {
      setIsOwner(true);
    }
  }, [ownerId, user?.id]);

  const generateNonce = async () => {
    if (!token) {
      console.error("Токен отсутствует в localStorage");
      return null;
    }
    try {
      console.log("Отправка запроса на nonce с token:", token);
      const response = await fetch(`/api/gdz/${number}/purchase`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Response status:", response.status, errorData);
        throw new Error(errorData.detail || "Ошибка генерации nonce");
      }
      const data = await response.json();
      return data.confirmation_code;
    } catch (error) {
      console.error("Ошибка генерации nonce:", error);
      return null;
    }
  };

  const handleCardClick = () => {
    navigate(`/category/${slug}/${number}`);
  };

  const handleButtonClick = async () => {
    setError(null);
    setShowGdz(false);
    if (isOwner || price === 0 || has_purchased ) {
      setShowGdz(true);
      setModalActive(true);
    } else {
      const newNonce = await generateNonce();
      if (!newNonce) {
        setError(
          "Не удалось загрузить форму оплаты. Пожалуйста, войдите в систему или попробуйте снова."
        );
        return;
      }
      setNonce(newNonce);
      setModalActive(true);
    }
  };

  const closeModal = () => {
    setModalActive(false);
    setNonce(null);
    setError(null);
    setShowGdz(false);
  };

  const handlePaymentSuccess = () => {
    setShowGdz(true);
    setNonce(null);
  };

  return (
    <div className="hwPanel">
      <Modal active={modalActive} setActive={closeModal}>
        {error ? (
          <div>{error}</div>
        ) : showGdz || isOwner || price === 0 || has_purchased ? (
          <PreviewHomework gdzId={number} setActive={closeModal} />
        ) : nonce ? (
          <PaymentForm
            nonce={nonce}
            gdzId={number}
            onClose={closeModal}
            onSuccess={handlePaymentSuccess}
          />
        ) : (
          <div>Загрузка формы оплаты...</div>
        )}
      </Modal>

      <div className="taskText" onClick={handleCardClick}>
        {number && <h2 className="bold">Задача {number}</h2>}
        <TooltipText text={taskText} maxLength={36} as="h2" />
      </div>

      <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
{/*         {tag && <div className="taskTag">{tag}</div>} */}
        <button
          className="button"
          style={{ pointerEvents: "auto" }}
          onClick={handleButtonClick}
        >
          {isOwner ? "Просмотреть ГДЗ": has_purchased ? "Посмотреть ГДЗ" : price === 0 ? "Бесплатно" : price + " руб"}
        </button>
      </div>
    </div>
  );
};

export default HomeWorkPanel;