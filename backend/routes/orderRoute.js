import express from "express";
import { placeOrder, getUserOrders, getAllOrders, updateOrderStatus } from "../controllers/orderController.js";
import adminAuth from "../middleware/adminAuth.js";

const orderRouter = express.Router();

orderRouter.post("/place", placeOrder);
orderRouter.post("/user", getUserOrders);
orderRouter.get("/all", adminAuth, getAllOrders);
orderRouter.post("/update-status", adminAuth, updateOrderStatus);

export default orderRouter;
