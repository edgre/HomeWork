import { useState } from "react";
import "../../assets/styles/headers.css";
import Modal from "./modal";

const HeaderButtom1 = () => {
  const [modalActive, setModalActive] = useState(false);
  return (
    <header className="headerButtom">
      <Modal active={modalActive} setActive={setModalActive}>
        <h2>Привет</h2>
      </Modal>
      <div className="header-menu">
        <h3>
          {
            "Выбери категорию своего домашнего задания или опубликуй свои работы"
          }
        </h3>
      </div>
      <button className="button" onClick={() => setModalActive(true)}>
        Опубликовать
      </button>
    </header>
  );
};

export default HeaderButtom1;
