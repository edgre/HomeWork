import React from "react";
import LogoHorizontal from "../../assets/images/Logo-horizontal.svg";
import "../../assets/styles/headers.css";
import { Link } from "react-router-dom";

const HeaderTop = () => {
  return (
    <header className="headerTop">
      <div className="header-menu">
        <div>
          {
            "Выбери категорию своего домашнего задания или опубликуй свои работы, чтобы заработать на свою мечту"
          }
        </div>
      </div>
      <Link to="/">
        <button className="button">Опубликовать</button>
      </Link>
    </header>
  );
};

export default HeaderTop;
