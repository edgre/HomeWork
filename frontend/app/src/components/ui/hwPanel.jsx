import { Link } from "react-router-dom";
import TooltipText from "./tooltipText";
import "../../assets/styles/headers.css";
import "../../assets/styles/grid.css";
import "../../assets/styles/text.css";

const HomeWorkPanel = ({ number, taskText, tag }) => {
  return (
    <div className="hwPanel">
      <div className="taskText">
        <h2 className="bold">Задача {number}</h2>

        <TooltipText text={taskText} maxLength={50} as="h2" />
      </div>
      <div style={{ display: "flex", gap: "12px", allignItems: "center" }}>
        {tag && <div className="taskTag">{tag}</div>}
        <Link to="/home">
          <button className="button">Бесплатно</button>
        </Link>
      </div>
    </div>
  );
};

export default HomeWorkPanel;
