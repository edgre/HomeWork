import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { UserContext } from "../../contexts/UserContext";
import LogoHorizontal from "../../assets/images/Logo-horizontal.svg";
import LogoProfile from "../../assets/images/User.svg";
import "../../assets/styles/headers.css";

const HeaderTop = () => {
  const { user } = useContext(UserContext);

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
        {/* Выводим username с проверкой на существование */}
        <h3>{user.realname}</h3>
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