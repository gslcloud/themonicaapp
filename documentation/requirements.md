import HomePage from './components/HomePage';
import ProfilePage from './components/ProfilePage';

export default class FrontendRouter {
  constructor() {
    this.routeMap = {
      '/': HomePage,
      '/profile': ProfilePage,
    };
    this.currentComponent = null;
  }

  init() {
    window.addEventListener('load', this.route.bind(this));
    window.addEventListener('popstate', this.route.bind(this));
  }

  route() {
    const path = window.location.pathname;
    const Component = this.routeMap[path] || NotFoundPage;

    // Check if the current component matches the one for the current path
    if (this.currentComponent instanceof Component) return;

    // Create a new instance of the component or reuse existing instance
    this.currentComponent = this.currentComponent instanceof Component
      ? this.currentComponent
      : new Component();

    // Render the component
    this.currentComponent.render();
  }
}