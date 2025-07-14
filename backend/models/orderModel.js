import mongoose from "mongoose";
import productModel from "./productModel.js";

const orderSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: "user", required: true },
  products: [
    {
      product: { type: mongoose.Schema.Types.ObjectId, ref: "product", required: true },
      quantity: { type: Number, required: true },
      size: { type: String, required: true },
    }
  ],
  address: {
    street: { type: String, required: true },
    city: { type: String, required: true },
    state: { type: String, required: true },
    zip: { type: String, required: true },
    country: { type: String, required: true },
  },
  status: { type: String, enum: ["Placed", "Processing", "Shipped", "Delivered", "Cancelled"], default: "Placed" },
  createdAt: { type: Date, default: Date.now },
});

export default mongoose.model("Order", orderSchema);
