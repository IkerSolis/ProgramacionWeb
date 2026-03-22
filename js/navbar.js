export const Navbar = {
  props: ['tipo'],
  template: `
    <nav class="navbar navbar-expand-lg sticky-top" style="background-color: var(--purple-mid);">
        <div class="container-fluid">

            <a class="navbar-brand d-flex align-items-center" href="index.html" style="color: var(--white-off);">
            <img src="../img/logo.jpeg" alt="Logo" style="width: 60px; height: auto;" class="me-2">
            Nexus<span>Key</span>
            </a>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navegacion">
            <span class="navbar-toggler-icon"></span>
            </button>
                        
            <div class="collapse navbar-collapse" id="navegacion">
            <ul class="navbar-nav ms-auto">

                <li class="nav-item">
                <a class="nav-link" style="color: var(--white-off);" href="vistas/catalogo.html">Catálogo</a>
                </li>

                <li class="nav-item">
                <a class="nav-link" style="color: var(--white-off);" href="#redes">Redes Sociales</a>
                </li>

                <li class="nav-item">
                <a class="nav-link" style="color: var(--white-off);" href="vistas/login.html">Iniciar Sesión</a>
                </li>

                <li class="nav-item" v-if="tipo === 'admin'">
                <a class="nav-link active" style="color: var(--white-off);" href="../vistas/panel_administracion.html">
                    Panel de Administración
                </a>
                </li>

            </ul>
            </div>

        </div>
    </nav>
  `
}