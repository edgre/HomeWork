import React, { useState, useEffect } from "react";
import axios from "axios";
import "../../assets/styles/dropDown.css";
import "../../assets/styles/authPage.css";

const DropdownList = ({ onCategoryChange, onSubcategoryChange, initialCategory, initialSubcategory }) => {
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedSubcategory, setSelectedSubcategory] = useState("");
  const [categories, setCategories] = useState([]);
  const [subcategories, setSubcategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [subcategoriesLoading, setSubcategoriesLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setSelectedCategory(initialCategory || "");
    setSelectedSubcategory(initialSubcategory || "");
  }, [initialCategory, initialSubcategory]);

  useEffect(() => {
    const fetchCategories = async () => {
      setLoading(true);
      try {
        const response = await axios.get("api/category");
        setCategories(response.data);
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

  useEffect(() => {
    const controller = new AbortController();

    if (selectedCategory) {
      const fetchSubcategories = async () => {
        setSubcategoriesLoading(true);
        setSubcategories([]);

        try {
          const response = await axios.get(`api/subjects/${selectedCategory}`, {
            signal: controller.signal
          });

          if (Array.isArray(response.data)) {
            setSubcategories(response.data);
            setError(null);
          } else {
            throw new Error("Некорректный формат данных подкатегорий");
          }
        } catch (err) {
          if (!axios.isCancel(err)) {
            setError("Ошибка при загрузке предметов");
            console.error(err);
          }
        } finally {
          setSubcategoriesLoading(false);
        }
      };

      fetchSubcategories();
    } else {
      setSubcategories([]);
      setSelectedSubcategory("");
      onSubcategoryChange("");
    }

    return () => controller.abort();
  }, [selectedCategory, onSubcategoryChange]);

  const handleCategoryChange = (e) => {
    const value = e.target.value;
    setSelectedCategory(value);
    onCategoryChange(value);
  };

  const handleSubcategoryChange = (e) => {
    const value = e.target.value;
    setSelectedSubcategory(value);
    onSubcategoryChange(value);
  };

  const SkeletonLoader = ({ height = "40px", width = "100%" }) => (
    <div
      className="skeleton-loader"
      style={{
        height,
        width,
        backgroundColor: "#f0f0f0",
        borderRadius: "4px",
        animation: "pulse 1.5s infinite ease-in-out"
      }}
    />
  );

  return (
    <>
      <div className="form-group">
        {loading ? (
          <SkeletonLoader height="40px" />
        ) : (
          <select
            className="dropdown-select"
            value={selectedCategory}
            onChange={handleCategoryChange}
          >
            <option value="">Выберите категорию</option>
            {categories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        )}
        {error && <p className="error">{error}</p>}
      </div>

      <div className="form-group">
        {subcategoriesLoading ? (
          <SkeletonLoader height="40px" />
        ) : (
          <select
            className="dropdown-select"
            value={selectedSubcategory}
            onChange={handleSubcategoryChange}
            disabled={!selectedCategory}
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
        )}
      </div>
    </>
  );
};

export default DropdownList;