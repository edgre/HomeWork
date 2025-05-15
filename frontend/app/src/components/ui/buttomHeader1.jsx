import { useState } from "react";
import { Link } from "react-router-dom";
import "../../assets/styles/headers.css";
import Modal from "./modal";
import HomeworkCreate from "./hwCreate";

const HeaderButtom1 = () => {
  const [modalActive, setModalActive] = useState(false);
  return (
    <header className="headerButtom">
      {/* <Modal active={modalActive} setActive={setModalActive}>
        <HomeworkCreate />
      </Modal> */}
      <div className="header-menu">
        <h3>
          {
            "Выбери категорию своего домашнего задания или опубликуй свои работы"
          }
        </h3>
      </div>
      <Link to="/create">
        <button className="button" onClick={() => setModalActive(true)}>
          Опубликовать
        </button>
      </Link>
    </header>
  );
};

export default HeaderButtom1;
