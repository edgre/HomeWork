import React from "react";
import LogoHorizontal from "../../assets/images/Logo-horizontal.svg";
import LogoProfile from "../../assets/images/User.svg";
import "../../assets/styles/headers.css";
import { Link } from "react-router-dom";

const HeaderTop = ({ username }) => {
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
        <h3>{username}</h3>
        <Link to="/me">
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