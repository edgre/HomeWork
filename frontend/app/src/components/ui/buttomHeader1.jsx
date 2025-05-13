import "../../assets/styles/headers.css";
import { Link } from "react-router-dom";

const HeaderButtom1 = () => {
  return (
    <header className="headerButtom">
      <div className="header-menu">
        <div>
          {
            "Выбери категорию своего домашнего задания или опубликуй свои работы, чтобы заработать на свою мечту"
          }
        </div>
      </div>
      <Link to="/home">
        <button className="button">Опубликовать</button>
      </Link>
    </header>
  );
};

export default HeaderButtom1;
