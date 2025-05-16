import { useNavigate } from "react-router-dom";
import React, { useState, useRef, useEffect } from "react";
import "../assets/styles/grid.css";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom1 from "../components/ui/buttomHeader1";
import CapIcon from "../assets/images/GraduationCap.svg";
import ButtonWithIcon from "../components/ui/iconTextButton.jsx";

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

  const labWorksRef = useRef(null);
  const researchRef = useRef(null);
  const schoolRef = useRef(null);
  const universityRef = useRef(null);

  // Функция для загрузки данных из API
  const fetchSubjects = async (category) => {
    try {
      const response = await fetch(`/api/subjects/${category}`);
      if (!response.ok) {
        throw new Error(`Ошибка при загрузке ${category}`);
      }
      const data = await response.json();
      return data.map(item => ({
        name: item.subject_name,
        slug: item.slug
      }));
    } catch (err) {
      console.error(`Ошибка при загрузке ${category}:`, err);
      setError(err.message);
      return [];
    }
  };

  // Загрузка всех категорий при монтировании компонента
  useEffect(() => {
    const loadAllCategories = async () => {
      try {
        setLoading(true);

        const [labWorks, research, school, university] = await Promise.all([
          fetchSubjects("laboratoryWorks"),
          fetchSubjects("researchWorks"),
          fetchSubjects("schoolTasks"),
          fetchSubjects("universityTasks")
        ]);

        setCategories({
          laboratoryWorks: labWorks,
          researchWorks: research,
          schoolTasks: school,
          universityTasks: university
        });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadAllCategories();
  }, []);

  // Настройка горизонтального скролла (остается без изменений)
  useEffect(() => {
    const setupHorizontalScroll = (ref) => {
      if (!ref.current) return;

      ref.current.addEventListener("wheel", (event) => {
        if (event.deltaMode === event.DOM_DELTA_PIXEL) {
          var modifier = 1;
        } else if (event.deltaMode === event.DOM_DELTA_LINE) {
          var modifier = parseInt(getComputedStyle(ref.current).lineHeight);
        } else if (event.deltaMode === event.DOM_DELTA_PAGE) {
          var modifier = ref.current.clientHeight;
        }

        if (event.deltaY !== 0) {
          ref.current.scrollLeft += modifier * event.deltaY;
          event.preventDefault();
        }
      });
    };

    setupHorizontalScroll(labWorksRef);
    setupHorizontalScroll(researchRef);
    setupHorizontalScroll(schoolRef);
    setupHorizontalScroll(universityRef);

    return () => {
      [labWorksRef, researchRef, schoolRef, universityRef].forEach((ref) => {
        if (ref.current) {
          ref.current.removeEventListener("wheel");
        }
      });
    };
  }, []);

  const handleCardClick = (slug) => {
    navigate(`/category/${slug}`);
  };

  if (loading) {
    return <div className="loading">Загрузка...</div>;
  }

  if (error) {
    return <div className="error">Ошибка: {error}</div>;
  }

  return (
    <div className="">
      <header>
        <HeaderTop username={"Gleb"} />
        <HeaderButtom1 />
      </header>

      <div className="grid">
        <div className="row-complete">
          <div className="row-header">Школьный курс • Задачи</div>
          <div className="row-cards" ref={schoolRef}>
            {categories.schoolTasks.map((task, index) => (
              <button
                key={index}
                className="card"
                onClick={() => handleCardClick(task.slug)}
              >
                {task.name}
              </button>
            ))}
          </div>
        </div>

        <div className="row-complete">
          <div className="row-header">ВУЗ • Задачи</div>
          <div className="row-cards" ref={universityRef}>
            {categories.universityTasks.map((task, index) => (
              <button
                key={index}
                className="card"
                onClick={() => handleCardClick(task.slug)}
              >
                {task.name}
              </button>
            ))}
          </div>
        </div>

        <div className="row-complete">
          <div className="row-header">ВУЗ • Лабораторные работы</div>
          <div className="row-cards" ref={labWorksRef}>
            {categories.laboratoryWorks.map((work, index) => (
              <button
                key={index}
                className="card"
                onClick={() => handleCardClick(work.slug)}
              >
                {work.name}
              </button>
            ))}
          </div>
        </div>

        <div className="row-complete">
          <div className="row-header">ВУЗ • Исследовательские работы</div>
          <div className="row-cards" ref={researchRef}>
            {categories.researchWorks.map((work, index) => (
              <ButtonWithIcon
                icon={CapIcon}
                key={index}
                className="card"
                onClick={() => handleCardClick(work.slug)}
              >
                {work.name}
              </ButtonWithIcon>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;