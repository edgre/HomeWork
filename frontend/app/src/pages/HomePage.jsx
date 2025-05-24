import { useNavigate } from "react-router-dom";
import React, { useState, useRef, useEffect } from "react";
import "../assets/styles/grid.css";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom1 from "../components/ui/buttomHeader1";
import CapIcon from "../assets/images/GraduationCap.svg";
import ButtonWithIcon from "../components/ui/iconTextButton.jsx";

// Константы для названий категорий
const CATEGORY_TITLES = {
  laboratoryWorks: "ВУЗ • Лабораторные работы",
  researchWorks: "ВУЗ • Исследовательские работы",
  schoolTasks: "Школьный курс • Задачи",
  universityTasks: "ВУЗ • Задачи"
};

// Маппинг для строковых значений категорий
const CATEGORY_NAMES = {
  laboratoryWorks: "Лабораторные работы",
  researchWorks: "Научные работы",
  schoolTasks: "Школьные задачи",
  universityTasks: "Университетские задачи"
};

const HomePage = () => {
  const navigate = useNavigate();
  const [categories, setCategories] = useState({
    laboratoryWorks: [],
    researchWorks: [],
    schoolTasks: [],
    universityTasks: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refs = {
    laboratoryWorks: useRef(null),
    researchWorks: useRef(null),
    schoolTasks: useRef(null),
    universityTasks: useRef(null)
  };

  const fetchSubjects = async (category) => {
    try {
      const response = await fetch(`/api/subjects/${category}`);
      if (!response.ok) throw new Error(`Failed to load ${category}`);
      return await response.json();
    } catch (err) {
      console.error(`Error loading ${category}:`, err);
      setError(err.message);
      return [];
    }
  };

  useEffect(() => {
    const loadAllCategories = async () => {
      try {
        setLoading(true);

        const [labData, researchData, schoolData, universityData] = await Promise.all([
          fetchSubjects("Лабораторные работы"),
          fetchSubjects("Научные работы"),
          fetchSubjects("Школьные задачи"),
          fetchSubjects("Университетские задачи")
        ]);

        setCategories({
          laboratoryWorks: labData,
          researchWorks: researchData,
          schoolTasks: schoolData,
          universityTasks: universityData
        });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadAllCategories();
  }, []);

  useEffect(() => {
    const setupHorizontalScroll = (ref) => {
      if (!ref.current) return;

      const handleWheel = (event) => {
        if (event.deltaY !== 0) {
          ref.current.scrollLeft += event.deltaY;
          event.preventDefault();
        }
      };

      ref.current.addEventListener('wheel', handleWheel);
      return () => ref.current.removeEventListener('wheel', handleWheel);
    };

    Object.values(refs).forEach(ref => setupHorizontalScroll(ref));
  }, []);

  const handleCardClick = (category, subjectName) => {
    // Формируем slug как category_subject
    const combinedSlug = `${category}_${subjectName}`;
    navigate(`/category/${combinedSlug}`);
  };

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;

  return (
    <div className="">
      <header>
        <HeaderTop username={"Gleb"} />
        <HeaderButtom1 />
      </header>

      <div className="grid">
        {Object.entries(categories).map(([categoryKey, items]) => (
          <div className="row-complete" key={categoryKey}>
            <div className="row-header">{CATEGORY_TITLES[categoryKey]}</div>
            <div className="row-cards" ref={refs[categoryKey]}>
              {items.map((item, index) => (
                categoryKey === 'researchWorks' ? (
                  <ButtonWithIcon
                    icon={CapIcon}
                    key={index}
                    className="card"
                    onClick={() => handleCardClick(
                      CATEGORY_NAMES[categoryKey], // Используем строковое значение категории
                      item // item — строка
                    )}
                  >
                    {item} {/* Отображаем item как строку */}
                  </ButtonWithIcon>
                ) : (
                  <button
                    key={index}
                    className="card"
                    onClick={() => handleCardClick(
                      CATEGORY_NAMES[categoryKey], // Используем строковое значение категории
                      item // item — строка
                    )}
                  >
                    {item} {/* Отображаем item как строку */}
                  </button>
                )
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage;