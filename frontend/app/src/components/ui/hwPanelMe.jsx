import { useState } from "react";
import TooltipText from "./tooltipText";
import Modal from "./modal";
import PreviewHomework from "./previewHomework";
import "../../assets/styles/headers.css";
import "../../assets/styles/grid.css";
import "../../assets/styles/text.css";

const HomeWorkPanel = ({ subject, taskText }) => {
  const [modalActive, setModalActive] = useState(false);
  return (
    <div className="hwPanel">
      <Modal active={modalActive} setActive={setModalActive}>
        {/* <h1>Просмотр своего дз</h1> */}
        <PreviewHomework taskTextFull="Найти решение системы уравнений через китайскую теорему об остатках. Вывести ФСР." />
      </Modal>
      <div className="taskText">
        <h2 className="bold">{subject}</h2>
        <TooltipText text={taskText} maxLength={36} as="h2" />
      </div>
      <div style={{ display: "flex", gap: "12px", allignItems: "center" }}>
        <button className="button" onClick={() => setModalActive(true)}>
          Просмотр
        </button>
      </div>
    </div>
  );
};

export default HomeWorkPanel;
