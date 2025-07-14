import Order from "../models/orderModel.js";
import productModel from "../models/productModel.js";

// Place a new order
export const placeOrder = async (req, res) => {
  try {
    const { user, products, address } = req.body;
    if (!user || !products || !address) {
      return res.status(400).json({ success: false, message: "All fields are required" });
    }
    // Decrease product count for each product in the order
    for (const item of products) {
      await productModel.findByIdAndUpdate(
        item.product,
        { $inc: { count: -item.quantity } },
        { new: true }
      );
    }
    const order = new Order({ user, products, address });
    await order.save();
    res.status(201).json({ success: true, order });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get orders for a user
export const getUserOrders = async (req, res) => {
  try {
    const { userId } = req.body;
    const orders = await Order.find({ user: userId }).populate("products.product");
    res.status(200).json({ success: true, orders });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Admin: Get all orders
export const getAllOrders = async (req, res) => {
  try {
    const orders = await Order.find().populate("user").populate("products.product");
    res.status(200).json({ success: true, orders });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Admin: Update order status
export const updateOrderStatus = async (req, res) => {
  try {
    const { orderId, status } = req.body;
    const order = await Order.findByIdAndUpdate(orderId, { status }, { new: true });
    res.status(200).json({ success: true, order });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};
