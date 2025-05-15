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

const categoryData2 = {
  // ВУЗ Лабораторные работы
  "lab-programming": {
    title: "Программирование",
    type: "laboratoryWorks",
    categoryName: "Лабораторные работы",
  },
  "lab-secmodel": {
    title: "Модели безопасности",
    type: "laboratoryWorks",
    categoryName: "Лабораторные работы",
  },
  "lab-networks": {
    title: "Компьютерные сети",
    type: "laboratoryWorks",
    categoryName: "Лабораторные работы",
  },
  "lab-tchmk": {
    title: "ТЧМК",
    type: "laboratoryWorks",
    categoryName: "Лабораторные работы",
  },
  "lab-plangs": {
    title: "Языки программирования",
    type: "laboratoryWorks",
    categoryName: "Лабораторные работы",
  },

  // ВУЗ Научные работы
  coursework: {
    title: "Курсовая работа",
    type: "researchWorks",
    categoryName: "Научные работы",
  },
  research: {
    title: "Научно-исследовательская работа",
    type: "researchWorks",
    categoryName: "Научные работы",
  },
  diploma: {
    title: "Диплом",
    type: "researchWorks",
    categoryName: "Научные работы",
  },
  vkr: {
    title: "BKP",
    type: "researchWorks",
    categoryName: "Научные работы",
  },

  // Школьные задачи
  "school-algebra": {
    title: "Алгебра",
    type: "schoolTasks",
    categoryName: "Школьные задачи",
  },
  "school-geometry": {
    title: "Геометрия",
    type: "schoolTasks",
    categoryName: "Школьные задачи",
  },
  "school-physics": {
    title: "Физика",
    type: "schoolTasks",
    categoryName: "Школьные задачи",
  },
  "school-informatics": {
    title: "Информатика",
    type: "schoolTasks",
    categoryName: "Школьные задачи",
  },

  // ВУЗ Задачи
  "high-mathanalisis": {
    title: "Мат. анализ",
    type: "universityTasks",
    categoryName: "Университетские задачи",
  },
  "high-economics": {
    title: "Экономика",
    type: "universityTasks",
    categoryName: "Университетские задачи",
  },
  "high-kmzi": {
    title: "КМЗИ",
    type: "universityTasks",
    categoryName: "Университетские задачи",
  },
  "high-cryptography": {
    title: "Криптография",
    type: "universityTasks",
    categoryName: "Университетские задачи",
  },
  "high-statistics": {
    title: "Мат. статистика",
    type: "universityTasks",
    categoryName: "Университетские задачи",
  },
  "high-probability": {
    title: "Теория вероятности",
    type: "universityTasks",
    categoryName: "Университетские задачи",
  },
  "high-algebra": {
    title: "Алгебра",
    type: "universityTasks",
    categoryName: "Университетские задачи",
  },
  "high-programming": {
    title: "Программирование",
    type: "universityTasks",
    categoryName: "Университетские задачи",
  },
};

const CategoryPage = () => {
  const { slug } = useParams(); // Берём айди страницы
  const navigate = useNavigate();
  const category = categoryData2[slug];

  const handleCardClick = (slug, hwid) => {
    navigate(`/category/${slug}/${hwid}`);
  };

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
        <HeaderTop username={"Gleb"} />
        <HeaderButtom2 />
      </header>

      <div className="grid">
        <div className="taskText">
          <h2 class="bold">{category.title}</h2>
          <h2 className="category-type-badge">{category.categoryName}</h2>
        </div>

        <HomeWorkPanel
          number={"1"}
          taskText={"Решить систему уравнений"}
          tag={"New"}
          price={"120"}
        />
        <HomeWorkPanel
          number={"2"}
          taskText={
            "Методом гаусса найти определитель матрицы альфа и бетта и гамма"
          }
          tag={"New"}
          price={"0"}
        />
      </div>
    </div>
  );
};

export default CategoryPage;
