import { useState, useEffect, useContext } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { UserContext } from "../../contexts/UserContext";
import TooltipText from "./tooltipText";
import Modal from "./modal";
import PaymentForm from "./paymentForm";
import PreviewHomework from "./previewHomework";
import "../../assets/styles/headers.css";
import "../../assets/styles/grid.css";
import "../../assets/styles/text.css";

const HomeWorkPanel = ({
  number,
  taskText,
  price,
  ownerId,
  has_purchased,
  gdzId,
  returnPath,
}) => {
  const [modalActive, setModalActive] = useState(false);
  const [nonce, setNonce] = useState(null);
  const [error, setError] = useState(null);
  const [showGdz, setShowGdz] = useState(false);
  const [isOwner, setIsOwner] = useState(false);
  const [localHasPurchased, setLocalHasPurchased] = useState(has_purchased); // Добавляем локальное состояние
  const { slug } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useContext(UserContext);
  const token = localStorage.getItem("access_token");

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

  const registerFreePurchase = async () => {
    try {
      const response = await fetch(`/api/gdz/${number}/free-purchase`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error("Не удалось зарегистрировать бесплатную покупку");
      }
      return await response.json();
    } catch (error) {
      console.error("Ошибка регистрации бесплатной покупки:", error);
      return null;
    }
  };

  const handleButtonClick = async () => {
    setError(null);
    setShowGdz(false);

    const currentPath = returnPath || location.pathname;
    localStorage.setItem("returnPath", currentPath);

    if (isOwner || price === 0 || localHasPurchased) {
      if (price === 0 && !localHasPurchased && !isOwner) {
        await registerFreePurchase();
        setLocalHasPurchased(true); // Обновляем состояние после успешной покупки
      }
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

    const savedPath = localStorage.getItem("returnPath");
    if (savedPath) {
      navigate(savedPath);
      localStorage.removeItem("returnPath");
    }
  };

  const handlePaymentSuccess = () => {
    setLocalHasPurchased(true);
    setShowGdz(true);
    setNonce(null);
  };

  return (
    <div className="hwPanel">
      <Modal active={modalActive} setActive={closeModal}>
        {error ? (
          <div>{error}</div>
        ) : showGdz || isOwner || price === 0 || localHasPurchased ? (
          <PreviewHomework
            gdzId={gdzId || number}
            setActive={closeModal}
            onClose={closeModal}
          />
        ) : nonce ? (
          <PaymentForm
            nonce={nonce}
            gdzId={gdzId || number}
            onClose={closeModal}
            onSuccess={handlePaymentSuccess}
          />
        ) : (
          <div>Загрузка формы оплаты...</div>
        )}
      </Modal>

      <div className="taskText">
        {number && <h2 className="bold">Задача {number}</h2>}
        <TooltipText text={taskText} maxLength={36} as="h2" />
      </div>

      <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
        <button
          className="button"
          style={{ pointerEvents: "auto" }}
          onClick={handleButtonClick}
        >
          {isOwner
            ? "Просмотреть ГДЗ"
            : localHasPurchased
            ? "Посмотреть ГДЗ"
            : price === 0
            ? "Бесплатно"
            : price + " руб"}
        </button>
      </div>
    </div>
  );
};

export default HomeWorkPanel;
