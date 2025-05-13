import React from "react";
import ArrowLeft from "../../assets/images/ArrowLeft.svg";
import ButtonWithIcon from "../ui/iconTextButton";
import "../../assets/styles/headers.css";
import { Link } from "react-router-dom";

const HeaderTop = () => {
  return (
    <header className="headerTop">
      <Link to="/">
        <ButtonWithIcon icon={ArrowLeft} className={buttonGrey}>
          Назад
        </ButtonWithIcon>
      </Link>
      <div className="header-menu">
        <Link to="/">
          <button className="button">Опубликовать</button>
        </Link>
      </div>
    </header>
  );
};

export default HeaderTop;
