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
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;

  const parseSlug = (slug) => {
    const [firstPart, ...restParts] = slug.split("_");
    const title = firstPart;
    const category = restParts.join(" ");
    return { title, category };
  };

  const { title, category } = parseSlug(slug);

  useEffect(() => {
    const loadTasks = async () => {
      try {
        setIsLoading(true);
        const token = localStorage.getItem("access_token");
        console.log("Токен:", token);
        const headers = { Authorization: `Bearer ${token}` };

        const response = await fetch(`/api/gdz_category/${encodeURIComponent(slug)}`, {
          headers,
        });

        if (!response.ok) {
          if (response.status === 401) {
            setError("Пожалуйста, войдите в систему");
            return;
          }
          throw new Error(`Ошибка загрузки: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("Данные задач из API:", data);
        console.log("Количество задач:", data.length);
        setTasks(data || []);
      } catch (err) {
        setError(err.message);
        console.error("Ошибка:", err);
      } finally {
        setIsLoading(false);
      }
    };
    loadTasks();
  }, [slug, navigate]);

  const totalPages = Math.ceil(tasks.length / pageSize);
  console.log("tasks.length:", tasks.length, "pageSize:", pageSize, "totalPages:", totalPages);
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  const paginatedTasks = tasks.slice(startIndex, endIndex);

  const goToNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const goToPrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const goToPage = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  if (isLoading) return <div className="loading-spinner">Загрузка...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="category-page page-container">
      <header>
        <HeaderTop />
        <HeaderButtom2 />
      </header>

      <div className="grid">
        <div className="taskText">
          <h2 className="bold">{title}</h2>
          <h2 className="category-type-badge">{category}</h2>
        </div>

        {paginatedTasks.length > 0 ? (
          paginatedTasks.map((task) => (
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

        {tasks.length > pageSize && (
          <div className="pagination">
            <button
              onClick={goToPrevPage}
              disabled={currentPage === 1}
              className="pagination-button"
              aria-label="Предыдущая страница"
            >
              Назад
            </button>
            <div className="pagination-pages">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                  key={page}
                  onClick={() => goToPage(page)}
                  className={`pagination-button pagination-page ${currentPage === page ? "active" : ""}`}
                  aria-label={`Перейти на страницу ${page}`}
                  aria-current={currentPage === page ? "page" : undefined}
                >
                  {page}
                </button>
              ))}
            </div>
            <button
              onClick={goToNextPage}
              disabled={currentPage === totalPages}
              className="pagination-button"
              aria-label="Следующая страница"
            >
              Вперед
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default CategoryPage;