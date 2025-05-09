import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div>
      <h1>{"Home Page"}</h1>
      <p>In progress... Go away!</p>
      <Link to={"/"}>
        <button className="button">Home</button>
      </Link>
    </div>
  );
};

export default HomePage;
