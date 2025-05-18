import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import TooltipText from "./tooltipText";
import Modal from "./modal";
import PaymentForm from "./paymentForm";
import PreviewHomework from "./previewHomework";
import "../../assets/styles/headers.css";
import "../../assets/styles/grid.css";
import "../../assets/styles/text.css";

const HomeWorkPanel = ({ number, taskText, price, tag, hwid }) => {
  const [modalActive, setModalActive] = useState(false);
  const { slug } = useParams(); // Берём айди страницы
  const navigate = useNavigate();

  const handleCardClick = (slug) => {
    navigate(`/category/${slug}/${hwid}`);
  };
  return (
    <div className="hwPanel">
      {price == 0 ? (
        <Modal active={modalActive} setActive={setModalActive}>
          <PreviewHomework
            taskTextFull={"Полное описание задачи"}
            setActive={setModalActive}
          />
        </Modal>
      ) : (
        <Modal active={modalActive} setActive={setModalActive}>
          {/* здесь нужно генерить нонсы */}
          <PaymentForm nonce="12b71v80n4c2j" />
        </Modal>
      )}

      <div className="taskText" onClick={() => handleCardClick()}>
        {number && <h2 className="bold">Задача {number}</h2>}

        <TooltipText text={taskText} maxLength={36} as="h2" />
      </div>

      <div style={{ display: "flex", gap: "12px", allignItems: "center" }}>
        {tag && <div className="taskTag">{tag}</div>}

        <button
          className="button"
          style={{ pointerEvents: "auto" }}
          onClick={() => setModalActive(true)}
        >
          {price == 0 ? "Бесплатно" : price + " руб"}
        </button>
      </div>
    </div>
  );
};

export default HomeWorkPanel;