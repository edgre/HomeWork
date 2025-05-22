import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom2 from "../components/ui/buttomHeader2";
import HomeWorkPanel from "../components/ui/hwPanel";
import "../assets/styles/grid.css";

const CategoryPage = () => {
  const { slug } = useParams(); // Например: "программирование лабораторные" или "lab-programming"
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Разбиваем slug на title и category
  const parseSlug = (slug) => {
    // Разделяем по первому пробелу
    const [firstPart, ...restParts] = slug.split("_");
    const title = firstPart;
    const category = restParts.join(" ")

    return {
      title: title,
      category: category,
    };
  };

  const { title, category } = parseSlug(slug);

  useEffect(() => {
  const loadTasks = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`/api/gdz_category/${encodeURIComponent(slug)}`);
      if (!response.ok) throw new Error("Ошибка загрузки");

      const data = await response.json();
      setTasks(data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };
  loadTasks();
}, [slug]);

  if (isLoading) return <div className="loading-spinner">Загрузка...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="category-page">
      <header>
        <HeaderTop username={"Gleb"} />
        <HeaderButtom2 />
      </header>

      <div className="grid">
        <div className="taskText">
          <h2 className="bold">{title}</h2>
          <h2 className="category-type-badge">{category}</h2>
        </div>

        {tasks.length > 0 ? (
          tasks.map((task) => (
            <HomeWorkPanel
              key={task.id}
              number={task.id}
              taskText={task.description}
//               tag={task.tag}
              price={task.price}
            />
          ))
        ) : (
          <p>Заданий пока нет</p>
        )}
      </div>
    </div>
  );
};

export default CategoryPage;