import { Link } from "react-router-dom";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom2 from "../components/ui/buttomHeader2";
import HomeworkCard from "../components/ui/hwCard";

import "../assets/styles/grid.css";

const TaskPage = () => {
  return (
    <div>
      <HeaderTop username={"Gleb"} />
      <HeaderButtom2 />

      <div className="grid">
        <HomeworkCard
          number={12}
          taskText={
            "Решить систему уравнений методом китайской теоремы об остатках"
          }
          taskTextFull={"Очень полное описание задачи с представлением формул"}
          price={"150"}
          tag={"New"}
        />
      </div>
    </div>
  );
};

export default TaskPage;
