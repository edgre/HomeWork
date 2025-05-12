import React from "react";
import LogoHorizontal from "../../assets/images/Logo-horizontal.svg";
import LogoProfile from "../../assets/images/User.svg";
import "../../assets/styles/headers.css";
import { Link } from "react-router-dom";

const HeaderTop = () => {
  return (
    <header className="headerTop">
      <div className="">
        <Link to="/home">
          <img
            className="icon-button"
            src={LogoHorizontal}
            width="298"
            height="48"
            alt="Домашка Плюс"
            loading="lazy"
          />
        </Link>
      </div>
      <nav className="header-menu">
        <Link>
          <img
            className="icon-button"
            src={LogoProfile}
            width="32"
            alt="Мой профиль"
            loading="lazy"
          />
        </Link>
        <Link to="/">
          <button className="buttonWhite">Выйти</button>
        </Link>
      </nav>
    </header>
  );
};

export default HeaderTop;
