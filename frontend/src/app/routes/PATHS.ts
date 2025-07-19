// this page doesnt talk about authorisation

const ROUTE_PARAMS = {
  userUsername: `:userUsername`,
  productId: `:productId`,
  orderId: `:orderId`,
  groupId: `:groupId`,
};

const PUBLIC_PATHS = {
  HOME: '',
  SIGN_UP: 'sign-up',
  SIGN_IN: 'sign-in',
  BUY: {
    ROOT: 'buy', // PRODUCT_ALL
    PRODUCT_ONE: (productId = `:productId`) => `${productId}`,
  },
  // put user_shop below because need specific routes first
  USER_SHOP: (userUsername = `:userUsername`) => `${userUsername}`,
  SERVER: `server-error`,
  ERROR: '**',
};

const USER_PATHS = {
  USER: (userUsername = `:userUsername`) => `${userUsername}`,
  ABOUT: {
    ROOT: `about`, // profile full details
    EDIT_PROFILE: `edit-profile`,
    EDIT_PASSWORD: `edit-password`,
  },
  GROUP: {
    ROOT: `groups`,
    CREATE_GROUP: `create`,
    EDIT_GROUP: (groupId = `:groupId`) => `${groupId}`,
  },
  BUYER_CART: {
    ROOT: `cart`,
    CHECKOUT: `checkout`,
  },
  BUYER_ORDERS: {
    ROOT: `orders`, // orders
    ORDER_ONE: (orderId = `:orderId`) => `${orderId}`,
  },
  SELLER: {
    ROOT: `sell`,
    PRODUCTS: {
      ROOT: `products`, // PRODUCT_ALL editable list of items user is selling
      PRODUCT_ONE: (productId = `:productId`) => `${productId}`,
    },
    ORDERS: {
      ROOT: `orders`, // ORDER_ALL
      ORDER_ONE: (orderId = `:orderId`) => `${orderId}`,
    },
  },
};

const URLS = {
  PUBLIC: {
    HOME: '/',
    SIGN_UP: `/${PUBLIC_PATHS.SIGN_UP}`,
    SIGN_IN: `/${PUBLIC_PATHS.SIGN_IN}`,
    BUY: {
      PRODUCT_ALL: `/${PUBLIC_PATHS.BUY.ROOT}`,
      PRODUCT_ONE: (productId: string) =>
        `/${PUBLIC_PATHS.BUY.ROOT}/${PUBLIC_PATHS.BUY.PRODUCT_ONE(productId)}`,
    },
    USER_SHOP: (userUsername: string) =>
      `/${PUBLIC_PATHS.USER_SHOP(userUsername)}`, // list of items user is selling
  },
  USER: (userUsername = `:userUsername`) => {
    const root_about = `/${userUsername}/${USER_PATHS.ABOUT.ROOT}`;
    const root_group = `/${userUsername}/${USER_PATHS.GROUP.ROOT}`;
    const root_buyerCart = `/${userUsername}/${USER_PATHS.BUYER_CART.ROOT}`;
    const root_buyerOrders = `/${userUsername}/${USER_PATHS.BUYER_ORDERS.ROOT}`;
    const root_seller = `/${userUsername}/${USER_PATHS.SELLER.ROOT}`;
    const root_seller_products = `/${userUsername}/${USER_PATHS.SELLER.ROOT}/${USER_PATHS.SELLER.PRODUCTS.ROOT}`;
    const root_seller_orders = `/${userUsername}/${USER_PATHS.SELLER.ROOT}/${USER_PATHS.SELLER.ORDERS.ROOT}`;

    return {
      ABOUT: {
        DEFAULT: root_about, // profile full details
        EDIT_PROFILE: `${root_about}/${USER_PATHS.ABOUT.EDIT_PROFILE}`,
        EDIT_PASSWORD: `${root_about}/${USER_PATHS.ABOUT.EDIT_PASSWORD}`,
      },
      GROUP: {
        DEFAULT: root_group,
        CREATE_GROUP: `${root_group}/${USER_PATHS.GROUP.CREATE_GROUP}`,
        EDIT_GROUP: (groupId: string) =>
          `${root_group}/${USER_PATHS.GROUP.EDIT_GROUP(groupId)}`,
      },
      BUYER_CART: {
        CART: root_buyerCart,
        CHECKOUT: `${root_buyerCart}/${USER_PATHS.BUYER_CART.CHECKOUT}`,
      },
      BUYER_ORDERS: {
        ORDERS_ALL: root_buyerOrders,
        ORDER_ONE: (orderId: string) =>
          `${root_buyerOrders}/${USER_PATHS.BUYER_ORDERS.ORDER_ONE(orderId)}`,
      },
      SELLER: {
        DEFAULT: root_seller,
        PRODUCT_ALL: `${root_seller_products}`,
        PRODUCT_ONE: (productId: string) =>
          `${root_seller_products}/${USER_PATHS.SELLER.PRODUCTS.PRODUCT_ONE(
            productId
          )}`,
        ORDER_ALL: `${root_seller_orders}`,
        ORDER_ONE: (orderId: string) =>
          `${root_seller_orders}/${USER_PATHS.SELLER.ORDERS.ORDER_ONE(
            orderId
          )}`,
      },
    };
  },
};

export { PUBLIC_PATHS, USER_PATHS, URLS };
