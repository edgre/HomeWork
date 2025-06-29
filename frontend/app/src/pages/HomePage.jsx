import { useNavigate } from "react-router-dom";
import React, { useState, useRef, useEffect, useContext } from "react";
import "../assets/styles/grid.css";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom1 from "../components/ui/buttomHeader1";
import CapIcon from "../assets/images/GraduationCap.svg";
import ButtonWithIcon from "../components/ui/iconTextButton.jsx";
import { UserContext } from "../contexts/UserContext";

// Названия для отображения заголовков блоков
const CATEGORY_TITLES = {
    laboratoryWorks: "ВУЗ • Лабораторные работы",
    schoolTasks: "Школьный курс • Задачи",
    universityTasks: "ВУЗ • Задачи",
    memology: "Мемология"
};

// Названия для API
const CATEGORY_NAMES = {
    laboratoryWorks: "Лабораторные работы",
    schoolTasks: "Школьные задачи",
    universityTasks: "Университетские задачи",
    memology: "Мемология"
};

const HomePage = () => {
    const navigate = useNavigate();
    const { user } = useContext(UserContext);
    const [categories, setCategories] = useState({
        laboratoryWorks: [],
        schoolTasks: [],
        universityTasks: [],
        memology: []

    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const refs = {
        laboratoryWorks: useRef(null),
        schoolTasks: useRef(null),
        universityTasks: useRef(null),
        memology: useRef(null)

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
                const [labData, schoolData, universityData, memData] = await Promise.all([
                    fetchSubjects(CATEGORY_NAMES.laboratoryWorks),
                    fetchSubjects(CATEGORY_NAMES.schoolTasks),
                    fetchSubjects(CATEGORY_NAMES.universityTasks),
                    fetchSubjects(CATEGORY_NAMES.memology)


                ]);

                setCategories({
                    laboratoryWorks: labData,
                    schoolTasks: schoolData,
                    universityTasks: universityData,
                    memology: memData
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

  const handleCardClick = (categoryName, subjectName) => {
  const combinedSlug = `${categoryName}_${subjectName}`;
  if (!user) {
    navigate("/", {
      state: {
        from: { pathname: `/category/${combinedSlug}` }
      }
    });
    return;
  }
  navigate(`/category/${combinedSlug}`);
};

    if (loading) return <div className="loading">Загрузка...</div>;
    if (error) return <div className="error">Ошибка: {error}</div>;

    return (
        <div>
            <header>
                <HeaderTop username={user?.username || "Гость"} />
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
                                        onClick={() => handleCardClick(CATEGORY_NAMES[categoryKey], item)}
                                    >
                                        {item}
                                    </ButtonWithIcon>
                                ) : (
                                        <button
                                            key={index}
                                            className="card"
                                            onClick={() => handleCardClick(CATEGORY_NAMES[categoryKey], item)}
                                        >
                                            {item}
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
