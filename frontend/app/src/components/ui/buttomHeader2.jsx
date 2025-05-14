import { useState } from "react";
import { Link } from "react-router-dom";
import ArrowLeft from "../../assets/images/ArrowLeft.svg";
import ButtonWithIcon from "../ui/iconTextButton";
import Modal from "./modal";

const HeaderButtom2 = () => {
  const [modalActive, setModalActive] = useState(false);
  return (
    <header className="headerButtom">
      <Modal active={modalActive} setActive={setModalActive}>
        <h2>Привет</h2>
      </Modal>
      <Link to="/home">
        <ButtonWithIcon icon={ArrowLeft} className="buttonGrey">
          Назад
        </ButtonWithIcon>
      </Link>

      <button className="button" onClick={() => setModalActive(true)}>
        Опубликовать
      </button>
    </header>
  );
};

export default HeaderButtom2;
