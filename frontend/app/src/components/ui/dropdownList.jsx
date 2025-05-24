import React, { useState, useEffect } from "react";
import axios from "axios";
import "../../assets/styles/dropDown.css";
import "../../assets/styles/authPage.css";

const DropdownList = ({ onCategoryChange, onSubcategoryChange, initialCategory, initialSubcategory }) => {
  const [selectedCategory, setSelectedCategory] = useState(initialCategory || "");
  const [selectedSubcategory, setSelectedSubcategory] = useState(initialSubcategory || "");
  const [categories, setCategories] = useState([]);
  const [subcategories, setSubcategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Загрузка категорий при монтировании компонента
  useEffect(() => {
    const fetchCategories = async () => {
      setLoading(true);
      try {
        const response = await axios.get("api/category");
        setCategories(response.data); // Предполагаем, что возвращается массив строк
        setError(null);
      } catch (err) {
        setError("Ошибка при загрузке категорий");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  // Синхронизация начальных значений
  useEffect(() => {
    if (initialCategory && initialCategory !== selectedCategory) {
      setSelectedCategory(initialCategory);
      onCategoryChange(initialCategory);
    }
    if (initialSubcategory && initialSubcategory !== selectedSubcategory) {
      setSelectedSubcategory(initialSubcategory);
      onSubcategoryChange(initialSubcategory);
    }
  }, [initialCategory, initialSubcategory, onCategoryChange, onSubcategoryChange]);

  // Загрузка подкатегорий при изменении selectedCategory
  useEffect(() => {
    if (selectedCategory) {
      const fetchSubcategories = async () => {
        setLoading(true);
        try {
          const response = await axios.get(`api/subjects/${selectedCategory}`);
          setSubcategories(response.data); // Предполагаем, что возвращается массив строк
          setError(null);

          // Если initialSubcategory есть, но не входит в новый список подкатегорий, сбрасываем её
          if (initialSubcategory && !response.data.includes(initialSubcategory)) {
            setSelectedSubcategory("");
            onSubcategoryChange("");
          }
        } catch (err) {
          setError("Ошибка при загрузке предметов");
          console.error(err);
        } finally {
          setLoading(false);
        }
      };

      fetchSubcategories();
    } else {
      setSubcategories([]);
      setSelectedSubcategory("");
      onSubcategoryChange("");
    }
  }, [selectedCategory, initialSubcategory, onSubcategoryChange]);

  const handleCategoryChange = (e) => {
    const value = e.target.value;
    setSelectedCategory(value);
    setSelectedSubcategory(""); // Сбрасываем подкатегорию при смене категории
    onCategoryChange(value);
    onSubcategoryChange(""); // Сбрасываем подкатегорию в родительском компоненте
  };

  const handleSubcategoryChange = (e) => {
    const value = e.target.value;
    setSelectedSubcategory(value);
    onSubcategoryChange(value);
  };

  return (
    <>
      <div className="form-group">
        <select
          className="dropdown-select"
          value={selectedCategory}
          onChange={handleCategoryChange}
          disabled={loading}
        >
          <option value="">Выберите категорию</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>
        {loading && <p>Загрузка...</p>}
        {error && <p className="error">{error}</p>}
      </div>

      <div className="form-group">
        <select
          className="dropdown-select"
          value={selectedSubcategory}
          onChange={handleSubcategoryChange}
          disabled={!selectedCategory || loading}
        >
          <option value="">
            {selectedCategory ? "Выберите предмет" : "Сначала выберите категорию"}
          </option>
          {subcategories.map((subcategory) => (
            <option key={subcategory} value={subcategory}>
              {subcategory}
            </option>
          ))}
        </select>
      </div>
    </>
  );
};

export default DropdownList;