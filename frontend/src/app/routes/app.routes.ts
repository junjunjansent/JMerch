import { Routes } from '@angular/router';
import { PUBLIC_PATHS } from './PATHS';
import { USER_PATHS } from './PATHS';
import HomeComponent from '../features/public/auth/home.component';
import { SignUpComponent } from '../features/public/auth/sign-up.component';
import { SignInComponent } from '../features/public/auth/sign-in.component';
// import { HomeComponent } from '../../pages/public/register/home.component';
// import { SignUpComponent } from '../../pages/public/register/sign-up.component';
// import { SignInComponent } from '../../pages/public/register/sign-in.component';
// import { AboutMainComponent } from '../../pages/users/about/about-main.component';
// import { AboutEditProfileComponent } from '../../pages/users/about/about-edit-profile.component';
// import { AboutEditPasswordComponent } from '../../pages/users/about/about-edit-password.component';
// import { UnknownPageComponent } from '../../pages/errors/unknown-page.component';
// import { ServerErrorComponent } from '../../pages/errors/server-error.component';
// import { UserShopComponent } from '../../pages/users/user-shop.component';
// import { GroupMainComponent } from '../../pages/users/groups/group-main.component';
// import { GroupCreateComponent } from '../../pages/users/groups/group-create.component';
// import { GroupEditComponent } from '../../pages/users/groups/group-edit.component';
// import { ProductOneComponent } from '../../pages/public/shop/product-one.component';
// import { ProductAllComponent } from '../../pages/public/shop/product-all.component';
// import { CartComponent } from '../../pages/buyer/cart/cart.component';
// import { CheckoutComponent } from '../../pages/buyer/cart/checkout.component';
// import { BuyerOrderAllComponent } from '../../pages/buyer/orders/buyer-order-all.component';
// import { BuyerOrderOneComponent } from '../../pages/buyer/orders/buyer-order-one.component';
// import { SellManagerComponent } from '../../pages/seller/sell-manager.component';
// import { AuthGuard } from '../auth.guards';

export const routes: Routes = [
  { path: PUBLIC_PATHS.HOME, component: HomeComponent },
  { path: PUBLIC_PATHS.SIGN_UP, component: SignUpComponent },
  { path: PUBLIC_PATHS.SIGN_IN, component: SignInComponent },
  // {
  //   path: PUBLIC_PATHS.BUY.ROOT,
  //   children: [
  //     { path: '', component: ProductAllComponent },
  //     { path: PUBLIC_PATHS.BUY.PRODUCT_ONE(), component: ProductOneComponent },
  //   ],
  // },
  // { path: PUBLIC_PATHS.USER_SHOP(), component: UserShopComponent },
  // {
  //   path: USER_PATHS.USER(),
  //   canActivate: [AuthGuard],
  //   canActivateChild: [AuthGuard], //for all children
  //   children: [
  //     { path: '', component: UserShopComponent },
  //     {
  //       path: USER_PATHS.ABOUT.ROOT,
  //       children: [
  //         { path: '', component: AboutMainComponent },
  //         {
  //           path: USER_PATHS.ABOUT.EDIT_PROFILE,
  //           component: AboutEditProfileComponent,
  //         },
  //         {
  //           path: USER_PATHS.ABOUT.EDIT_PASSWORD,
  //           component: AboutEditPasswordComponent,
  //         },
  //       ],
  //     },
  //     {
  //       path: USER_PATHS.GROUP.ROOT,
  //       children: [
  //         { path: '', component: GroupMainComponent },
  //         {
  //           path: USER_PATHS.GROUP.CREATE_GROUP,
  //           component: GroupCreateComponent,
  //         },
  //         {
  //           path: USER_PATHS.GROUP.EDIT_GROUP(),
  //           component: GroupEditComponent,
  //         },
  //       ],
  //     },
  //     {
  //       path: USER_PATHS.BUYER_CART.ROOT,
  //       children: [
  //         { path: '', component: CartComponent },
  //         {
  //           path: USER_PATHS.BUYER_CART.CHECKOUT,
  //           component: CheckoutComponent,
  //         },
  //       ],
  //     },
  //     {
  //       path: USER_PATHS.BUYER_ORDERS.ROOT,
  //       children: [
  //         { path: '', component: BuyerOrderAllComponent },
  //         {
  //           path: USER_PATHS.BUYER_ORDERS.ORDER_ONE(),
  //           component: BuyerOrderOneComponent,
  //         },
  //       ],
  //     },
  //     {
  //       path: USER_PATHS.SELLER.ROOT,
  //       children: [{ path: '', component: SellManagerComponent }],
  //     },
  //   ],
  // },
  // { path: PUBLIC_PATHS.SERVER, component: ServerErrorComponent },
  // { path: PUBLIC_PATHS.ERROR, component: UnknownPageComponent },
];
