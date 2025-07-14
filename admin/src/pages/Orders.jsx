import React, { useEffect, useState } from 'react';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchOrders = async () => {
      setLoading(true);
      setError('');
      const token = localStorage.getItem('token');
      if (!token) {
        setError('Admin not logged in');
        setLoading(false);
        return;
      }
      try {
        const res = await fetch('http://localhost:4000/api/order/all', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();
        if (!res.ok) {
          setError(data.message || 'Failed to fetch orders');
        } else {
          setOrders(data.orders || []);
        }
      } catch (err) {
        setError('Network error');
      }
      setLoading(false);
    };
    fetchOrders();
  }, []);

  return (
    <div className='pt-16 border-t'>
      <h2 className='text-2xl mb-6'>All Orders</h2>
      {loading ? (
        <div className='my-8 text-center'>Loading...</div>
      ) : error ? (
        <div className='my-8 text-center text-red-500'>{error}</div>
      ) : orders.length === 0 ? (
        <div className='my-8 text-center'>No orders found.</div>
      ) : (
        <div>
          {orders.map((order, idx) => (
            <div key={order._id || idx} className='flex flex-col gap-4 py-4 text-gray-700 border-t border-b md:flex-row md:items-center md:justify-between'>
              <div className='flex flex-col gap-2'>
                <div className='font-medium'>Order ID: {order._id}</div>
                <div className='text-sm text-gray-500'>Placed: {new Date(order.createdAt).toLocaleString()}</div>
                <div className='text-sm'>Status: <span className='font-semibold'>{order.status}</span></div>
                <div className='text-sm'>User: {order.user && order.user.email}</div>
                <div className='text-sm'>Address: {order.address.street}, {order.address.city}, {order.address.state}, {order.address.zip}, {order.address.country}</div>
              </div>
              <div className='flex-1'>
                {order.products.map((item, i) => (
                  <div key={i} className='flex items-center gap-4 my-2'>
                    <img className='w-16 sm:w-20' src={item.product && item.product.image && item.product.image[0]} alt='Product' />
                    <div>
                      <p className='font-medium sm:text-base'>{item.product && item.product.name}</p>
                      <div className='flex items-center gap-3 mt-2 text-base text-gray-700'>
                        <p className='text-lg'>Qty: {item.quantity}</p>
                        <p>Size: {item.size}</p>
                        <p>Price: ₹{item.product && item.product.price}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Orders;