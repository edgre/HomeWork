import { useState } from "react";
import { Link } from "react-router-dom";
import ArrowLeft from "../../assets/images/ArrowLeft.svg";
import ButtonWithIcon from "../ui/iconTextButton";
import Modal from "./modal";
import HomeworkCreate from "./hwCreate";

const HeaderButtom2 = () => {
  const [modalActive, setModalActive] = useState(false);
  return (
    <header className="headerButtom">
      <Link to="/home">
        <ButtonWithIcon icon={ArrowLeft} className="buttonGrey">
          Назад
        </ButtonWithIcon>
      </Link>
      <Link to="/create">
        <button className="button" onClick={() => setModalActive(true)}>
          Опубликовать
        </button>
      </Link>
    </header>
  );
};

export default HeaderButtom2;
