import React, { useContext, useState } from 'react'
import Title from '../components/Title'
import CartTotal from '../components/CartTotal'
import { assets } from '../assets/assets'
import { ShopContext } from '../context/ShopContext'

const PlaceOrder = () => {
  const [method, setMethod] = useState('cod');
  const { cartItems, navigate, setCartItems } = useContext(ShopContext);
  const [address, setAddress] = useState({
    firstName: '',
    lastName: '',
    email: '',
    street: '',
    city: '',
    state: '',
    zip: '',
    country: '',
    mobile: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Prepare products for order
  const orderProducts = [];
  for (const productId in cartItems) {
    for (const size in cartItems[productId]) {
      if (cartItems[productId][size] > 0) {
        orderProducts.push({
          product: productId,
          quantity: cartItems[productId][size],
          size,
        });
      }
    }
  }

  const handleChange = (e) => {
    setAddress({ ...address, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    // Validate address fields
    for (const key in address) {
      if (!address[key]) {
        setError('All address fields are required');
        setLoading(false);
        return;
      }
    }
    if (orderProducts.length === 0) {
      setError('No products in cart');
      setLoading(false);
      return;
    }
    // Get user from localStorage
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || !user._id) {
      setError('You must be logged in to place an order');
      setLoading(false);
      return;
    }
    try {
      const res = await fetch('http://localhost:4000/api/order/place', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user: user._id,
          products: orderProducts,
          address: {
            street: address.street,
            city: address.city,
            state: address.state,
            zip: address.zip,
            country: address.country,
          },
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.message || 'Order failed');
      } else {
        // Clear cart
        setCartItems && setCartItems({});
        localStorage.removeItem('cartItems');
        navigate('/orders');
      }
    } catch (err) {
      setError('Network error');
    }
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className='flex flex-col justify-between gap-4 pt-5 sm:flex-row sm:pt-14 min-h-[80vh] border-t'>
      {/* Left Side Content */}
      <div className='flex flex-col w-full gap-4 sm:max-w-[480px]'>
        <div className='my-3 text-xl sm:text-2xl'>
          <Title text1={'DELIVERY'} text2={'INFORMATION'} />
        </div>
        {error && <div className='text-red-500'>{error}</div>}
        <div className='flex gap-3'>
          <input className='w-full px-4 py-2 border border-gray-300 rounded' type="text" name="firstName" value={address.firstName} onChange={handleChange} placeholder='First Name' required />
          <input className='w-full px-4 py-2 border border-gray-300 rounded' type="text" name="lastName" value={address.lastName} onChange={handleChange} placeholder='Last Name' required />
        </div>
        <input className='w-full px-4 py-2 border border-gray-300 rounded' type="email" name="email" value={address.email} onChange={handleChange} placeholder='Email Address' required />
        <input className='w-full px-4 py-2 border border-gray-300 rounded' type="text" name="street" value={address.street} onChange={handleChange} placeholder='Street' required />
        <div className='flex gap-3'>
          <input className='w-full px-4 py-2 border border-gray-300 rounded' type="text" name="city" value={address.city} onChange={handleChange} placeholder='City' required />
          <input className='w-full px-4 py-2 border border-gray-300 rounded' type="text" name="state" value={address.state} onChange={handleChange} placeholder='State' required />
        </div>
        <div className='flex gap-3'>
          <input className='w-full px-4 py-2 border border-gray-300 rounded' type="number" name="zip" value={address.zip} onChange={handleChange} placeholder='Zip Code' required />
          <input className='w-full px-4 py-2 border border-gray-300 rounded' type="text" name="country" value={address.country} onChange={handleChange} placeholder='Country' required />
        </div>
        <input className='w-full px-4 py-2 border border-gray-300 rounded' type="number" name="mobile" value={address.mobile} onChange={handleChange} placeholder='Mobile' required />
      </div>
      {/* Right Side Content */}
      <div className='mt-8'>
        <div className='mt-8 min-w-80'>
          <CartTotal />
        </div>
        {/* Payment Methods Selection */}
        <div className='mt-12'>
          <Title text1={'PAYMENT'} text2={'METHODS'} />
          <div className='flex flex-col gap-3 lg:flex-row'>
            <div onClick={() => setMethod('stripe')} className='flex items-center gap-3 p-2 px-3 border cursor-pointer'>
              <p className={`min-w-3.5 h-3.5 border rounded-full ${method === 'stripe' ? 'bg-green-600' : ''}`}></p>
              <img className='h-5 mx-4' src={assets.stripe_logo} alt="Stripe" />
            </div>
            <div onClick={() => setMethod('razorpay')} className='flex items-center gap-3 p-2 px-3 border cursor-pointer'>
              <p className={`min-w-3.5 h-3.5 border rounded-full ${method === 'razorpay' ? 'bg-green-600' : ''}`}></p>
              <img className='h-5 mx-4' src={assets.razorpay_logo} alt="RazorPay" />
            </div>
            <div onClick={() => setMethod('cod')} className='flex items-center gap-3 p-2 px-3 border cursor-pointer'>
              <p className={`min-w-3.5 h-3.5 border rounded-full ${method === 'cod' ? 'bg-green-600' : ''}`}></p>
              <p className='mx-4 text-sm font-medium text-gray-500'>CASH ON DELIVERY</p>
            </div>
          </div>
          <div className='w-full mt-8 text-end'>
            <button type="submit" className='px-16 py-3 text-sm text-white bg-black active:bg-gray-800' disabled={loading}>
              {loading ? 'Placing Order...' : 'PLACE ORDER'}
            </button>
          </div>
        </div>
      </div>
    </form>
  )
}

export default PlaceOrder
