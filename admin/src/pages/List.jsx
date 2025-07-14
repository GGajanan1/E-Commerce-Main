import React, { useEffect, useState } from "react";
import axios from "axios";
import { backendUrl, currency } from "../App";
import { toast } from "react-toastify";

const List = ({ token }) => {
  const [listProducts, setListProducts] = useState([]);
  const [editProduct, setEditProduct] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);

  const fetchListProducts = async () => {
    try {
      const response = await axios.get(backendUrl + "/api/product/list");

      if (response.data.success) {
        setListProducts(response.data.products);
      } else {
        toast.error(response.data.message);
      }
    } catch (error) {
      console.error(error);
      toast.error(response.data.message);
    }
  };

  const removeProduct = async (id) => {
    try {
      const response = await axios.post(
        backendUrl + "/api/product/remove",
        { id },
        { headers: { token } }
      );

      if (response.data.success) {
        toast.info(response.data.message);
        await fetchListProducts();
      } else {
        toast.error(response.data.message);
      }
    } catch (error) {
      console.error(error);
      toast.error(response.data.message);
    }
  };

  const handleEdit = (product) => {
    setEditProduct(product);
    setShowEditModal(true);
  };

  const handleSaveEdit = async () => {
    try {
      const response = await axios.post(
        backendUrl + "/api/product/update",
        {
          id: editProduct._id,
          name: editProduct.name,
          description: editProduct.description,
          price: editProduct.price,
          count: editProduct.count,
        },
        { headers: { token } }
      );
      if (response.data.success) {
        toast.success("Product updated");
        setShowEditModal(false);
        setEditProduct(null);
        await fetchListProducts();
      } else {
        toast.error(response.data.message);
      }
    } catch (error) {
      toast.error("Failed to update product");
    }
  };

  useEffect(() => {
    fetchListProducts();
  }, []);

  return (
    <>
      <div className="flex flex-col gap-2">
        {/* List Table Title */}
        <div className="hidden md:grid grid-cols-[0.5fr_1fr_1.5fr_0.5fr_0.5fr_0.5fr_0.5fr_0.2fr] items-center py-1 px-2 border bg-gray-200 text-xl text-center">
          <b>Image</b>
          <b>Name</b>
          <b>Description</b>
          <b>Category</b>
          <b>Sub Category</b>
          <b>Price</b>
          <b>Count</b>
          <b className="text-center">Action</b>
        </div>
        {/* Display Products */}
        {listProducts.map((item, index) => (
          <div
            className="grid grid-cols-[0.5fr_1fr_1.5fr_0.5fr_0.5fr_0.5fr_0.5fr_0.2fr] md:grid-cols-[0.5fr_1fr_1.5fr_0.5fr_0.5fr_0.5fr_0.5fr_0.2fr] items-center gap-2 py-1 px-2 border text-sm text-center"
            key={index}
          >
            <img className="w-12" src={item.image[0]} alt="Product Image" />
            <p className="text-left">{item.name}</p>
            <p className="text-left">{item.description}</p>
            <p>{item.category}</p>
            <p>{item.subCategory}</p>
            <p>{currency(item.price)}</p>
            <p>{item.count}</p>
            <button
              onClick={() => handleEdit(item)}
              className="px-2 py-1 text-xs text-white bg-blue-500 rounded mr-2"
            >
              Edit
            </button>
            <p
              onClick={() => removeProduct(item._id)}
              className="font-bold text-center text-gray-800 bg-red-500 rounded-full cursor-pointer md:text-center max-w-7"
            >
              X
            </p>
          </div>
        ))}
      </div>

      {showEditModal && editProduct && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
          <div className="bg-white p-6 rounded shadow-lg w-full max-w-md">
            <h2 className="text-xl mb-4">Edit Product</h2>
            <input
              className="w-full mb-2 px-2 py-1 border"
              value={editProduct.name}
              onChange={e => setEditProduct({ ...editProduct, name: e.target.value })}
              placeholder="Name"
            />
            <textarea
              className="w-full mb-2 px-2 py-1 border"
              value={editProduct.description}
              onChange={e => setEditProduct({ ...editProduct, description: e.target.value })}
              placeholder="Description"
            />
            <input
              className="w-full mb-2 px-2 py-1 border"
              value={editProduct.price}
              type="number"
              onChange={e => setEditProduct({ ...editProduct, price: e.target.value })}
              placeholder="Price"
            />
            <input
              className="w-full mb-2 px-2 py-1 border"
              value={editProduct.count}
              type="number"
              onChange={e => setEditProduct({ ...editProduct, count: e.target.value })}
              placeholder="Count"
            />
            <div className="flex gap-2 mt-4">
              <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={() => handleSaveEdit()}>Save</button>
              <button className="px-4 py-2 bg-gray-400 text-white rounded" onClick={() => setShowEditModal(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default List;
