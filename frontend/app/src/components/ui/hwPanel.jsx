import "../../assets/styles/headers.css";
import "../../assets/styles/grid.css";
import { Link } from "react-router-dom";

const HomeWorkPanel = () => {
  return (
    <div className="hwPanel">
      <div className="taskText">
        <h2 class="bold">Задача 3</h2>
        <h2>Короткая формулировка</h2>
      </div>
      {/* <div className="taskTag">тэг</div> */}
      <Link to="/home">
        <button className="button">Бесплатно</button>
      </Link>
    </div>
  );
};

export default HomeWorkPanel;
