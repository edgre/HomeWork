import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom2 from "../components/ui/buttomHeader2";
import HomeWorkPanel from "../components/ui/hwPanel";
import "../assets/styles/grid.css";

const CategoryPage = () => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const parseSlug = (slug) => {
    const [firstPart, ...restParts] = slug.split("_");
    const title = firstPart;
    const category = restParts.join(" ");

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
        const token = localStorage.getItem("access_token");
        const headers = { Authorization: `Bearer ${token}`};

        const response = await fetch(`/api/gdz_category/${encodeURIComponent(slug)}`, {
          headers,
        });

        if (!response.ok) {
          if (response.status === 401) {
            setError("Пожалуйста, войдите в систему");
            // Опционально: navigate("/login");
            return;
          }
          throw new Error(`Ошибка загрузки: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("Данные задач из API:", data);
        setTasks(data || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    loadTasks();
  }, [slug, navigate]);

  if (isLoading) return <div className="loading-spinner">Загрузка...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="category-page">
      <header>
        <HeaderTop />
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
              ownerId={task.owner_id}
              number={task.id}
              taskText={task.description}
              price={task.price}
              has_purchased={task.has_purchased}
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