import { Link } from "react-router-dom";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom2 from "../components/ui/buttomHeader2";
import HomeworkCreate from "../components/ui/hwCreate";

import "../assets/styles/grid.css";

const TaskPage = () => {
  return (
    <div>
      <HeaderTop username={"Gleb"} />
      <HomeworkCreate />
    </div>
  );
};

export default TaskPage;
