import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";

//CSS
import "../assets/styles/font.css";

//import '../src/styles/buttonRGB.css';
import "../assets/styles/buttons.css";
import "../assets/styles/colors.css";
import "../assets/styles/text.css";
import "../assets/styles/authPage.css";

const AuthPage = () => {
  const [username, setUsername] = useState("");
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [isRegistering, setIsRegistering] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const goToGame = () => {
    navigate("/home");
  };

  const validatePassword = (password) => {
    const minLength = password.length >= 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    if (!minLength) {
      return "Пароль должен содержать не менее 8 символов.";
    }
    if (!hasUpperCase) {
      return "Пароль должен содержать хотя бы одну заглавную букву.";
    }
    if (!hasLowerCase) {
      return "Пароль должен содержать хотя бы одну строчную букву.";
    }
    if (!hasNumber) {
      return "Пароль должен содержать хотя бы одну цифру.";
    }

    return "";
  };

  const handlePlayClick = () => {
    if (isRegistering) {
      if (!username || !login || !password) {
        setError("Пожалуйста, заполни все поля");
      } else {
        {
          const errorMessage = validatePassword(password);
          if (errorMessage) {
            setError(errorMessage);
          } else {
            goToGame();
            console.log("Username:", username);
            console.log("Login:", login);
            console.log("Password:", password);
          }
        }
      }
    } else {
      if (!login || !password) {
        setError("Пожалуйста, заполни все поля");
      } else {
        const errorMessage = validatePassword(password);
        if (errorMessage) {
          setError(errorMessage);
        } else {
          goToGame();
          console.log("Login:", login);
          console.log("Password:", password);
        }
      }
    }
  };

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };
  const handleLoginChange = (e) => {
    setLogin(e.target.value);
  };
  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };
  const toggleRegistration = () => {
    setIsRegistering(!isRegistering);
  };

  return (
    <div className="container">
      <div className="auth-form-container">
        <div
          className="h1"
          style={{ verticalAlign: "center", justifyContent: "center" }}
        >
          Добро пожаловать
        </div>
        <div className="h4" style={{ marginTop: "5px" }}>
          Пожалуйста пройди аутентификацию
        </div>

        <form className="auth-form" onSubmit={handlePlayClick}>
          <div className="form-group" style={{ padding: "0px" }}>
            <label className="switch">
              <input
                type="checkbox"
                checked={isRegistering}
                onChange={toggleRegistration}
              />
              <span className="slider">
                <span className="text-off">Войти</span>
                <span className="text-on">Регистрация</span>
              </span>
            </label>
          </div>

          {isRegistering && (
            <div className="form-group">
              <input
                type="text"
                id="username"
                className="inputBox"
                placeholder="Никнейм"
                value={username}
                onChange={handleUsernameChange}
                required
              />
            </div>
          )}

          <div className="form-group">
            <input
              type="text"
              id="login"
              className="inputBox"
              placeholder="Логин"
              value={login}
              onChange={handleLoginChange}
              required
            />
          </div>

          <div className="form-group">
            <input
              type="password"
              id="password"
              className="inputBox"
              placeholder="Пароль"
              value={password}
              onChange={handlePasswordChange}
              required
            />
          </div>

          <div className="form-group">
            <button
              onClick={(e) => {
                e.preventDefault();
                handlePlayClick();
              }}
              type="submit"
              className="buttonGreen"
              style={{ marginTop: "0px" }}
            >
              Играть
            </button>
          </div>
        </form>
      </div>
      {error && (
        <div className="auth-error-container">
          <div className="h5-error">{error}</div>
        </div>
      )}
    </div>
  );
};

export default AuthPage;
