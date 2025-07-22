import { HttpInterceptorFn } from '@angular/common/http';

// function based interceptor
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('token');
  if (token) {
    // console.log('sending HTTP request: ', `Bearer ${token}`);
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` },
    });
  }
  return next(req);
};

// // class based interceptor
// @Injectable()
// export class AuthInterceptor implements HttpInterceptor {
//   intercept(req: HttpRequest<any>, next: HttpHandler) {
//     const token = localStorage.getItem('token');
//     if (token) {
//       req = req.clone({
//         setHeaders: { Authorization: `Bearer ${token}` }
//       });
//     }
//     return next.handle(req);
//   }
// }
