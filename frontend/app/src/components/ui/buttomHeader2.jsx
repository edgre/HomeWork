import ArrowLeft from "../../assets/images/ArrowLeft.svg";
import ButtonWithIcon from "../ui/iconTextButton";
import { Link } from "react-router-dom";

const HeaderButtom2 = () => {
  return (
    <header className="headerButtom">
      <Link to="/home">
        <ButtonWithIcon icon={ArrowLeft} className="buttonGrey">
          Назад
        </ButtonWithIcon>
      </Link>

      <Link to="/home">
        <button className="button">Опубликовать</button>
      </Link>
    </header>
  );
};

export default HeaderButtom2;
