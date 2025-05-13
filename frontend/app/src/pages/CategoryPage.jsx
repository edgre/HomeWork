import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom2 from "../components/ui/buttomHeader2";
import HomeWorkPanel from "../components/ui/hwPanel";
import "../assets/styles/grid.css";

// import "../assets/styles/category.css";

const categoryData = {
  // Лабораторные работы
  programming: {
    title: "Программирование",
    type: "Лабораторные работы",
  },
  chemistry: {
    title: "Химия",
    type: "Лабораторные работы",
  },
  // Добавьте все остальные категории
};

const CategoryPage = () => {
  const { slug } = useParams(); // Берём айди страницы
  const navigate = useNavigate();
  const category = categoryData[slug];

  // В CategoryPage.jsx
  const [content, setContent] = useState(null);

  useEffect(() => {
    const loadContent = async () => {
      try {
        const response = await fetch(`/api/content/${slug}`);
        const data = await response.json();
        setContent(data);
      } catch (error) {
        console.error("Ошибка загрузки контента:", error);
      }
    };

    loadContent();
  }, [slug]);

  useEffect(() => {
    if (!category) {
      navigate("/not-found", { replace: true });
    }
  }, [category, navigate]);

  //   if (!category) return null;
  //   if (!content) return <div className="loading-spinner">Загрузка...</div>;

  return (
    <div className="category-page">
      <header>
        <HeaderTop />
        <HeaderButtom2 />
      </header>

      <div className="grid">
        <div className="taskText">
          <h2 class="bold">{category.title}</h2>
          <h2 className="category-type-badge">{category.type}</h2>
        </div>

        <HomeWorkPanel />
        <HomeWorkPanel />
      </div>
    </div>
  );
};

export default CategoryPage;
