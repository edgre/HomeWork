import { Link } from "react-router-dom";

const NotFoundPage = () => {
  return (
    <div>
      <h1> {"Not Found Page :("}</h1>
      <Link to={"/home"}>
        <button className="button">На главную</button>
      </Link>
    </div>
  );
};

export default NotFoundPage;
