<template>
  <div class="p-8 bg-gray-900 min-h-screen text-gray-100 font-sans">
    <div class="max-w-6xl mx-auto">
      <div class="flex justify-between items-center mb-8 border-b border-gray-800 pb-5">
        <div>
          <h1 class="text-2xl font-bold text-gray-100">Console de Administración Corporativa</h1>
          <p class="text-sm text-gray-400 mt-1">Gestión de infraestructura y cumplimiento operacional de la organización</p>
        </div>
        <span class="bg-red-500/10 border border-red-500/20 text-red-400 px-3 py-1.5 rounded-md text-xs font-mono">
          Modo: Administrador de Sistemas
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-gray-950 p-6 rounded-xl border border-gray-800">
          <div class="text-sm font-medium text-gray-400 mb-1">Usuarios Totales</div>
          <div class="text-3xl font-bold text-emerald-400">142</div>
        </div>
        <div class="bg-gray-950 p-6 rounded-xl border border-gray-800">
          <div class="text-sm font-medium text-gray-400 mb-1">Grupos/Departamentos</div>
          <div class="text-3xl font-bold text-blue-400">12</div>
        </div>
        <div class="bg-gray-950 p-6 rounded-xl border border-gray-800">
          <div class="text-sm font-medium text-gray-400 mb-1">Alertas de Seguridad (24h)</div>
          <div class="text-3xl font-bold text-yellow-500">0</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 bg-gray-950 p-6 rounded-xl border border-gray-800">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold text-gray-300">Directorio de Empleados</h2>
            <button class="bg-blue-600 hover:bg-blue-700 text-white text-xs px-3 py-1.5 rounded-md transition font-medium">
              + Dar de Alta Usuario
            </button>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-gray-400">
              <thead class="bg-gray-900 text-xs uppercase text-gray-500">
                <tr>
                  <th class="p-3">Email</th>
                  <th class="p-3">Rol</th>
                  <th class="p-3">Estado</th>
                  <th class="p-3 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-900">
                <tr class="hover:bg-gray-900/30">
                  <td class="p-3 font-medium text-gray-200">sistemas@empresa.local</td>
                  <td class="p-3"><span class="px-2 py-0.5 bg-purple-500/10 text-purple-400 text-xs rounded border border-purple-500/20">Admin</span></td>
                  <td class="p-3"><span class="text-emerald-400">● Activo</span></td>
                  <td class="p-3 text-right"><button class="text-gray-500 hover:text-gray-300">Editar</button></td>
                </tr>
                <tr class="hover:bg-gray-900/30">
                  <td class="p-3 font-medium text-gray-200">analista.financiero@empresa.local</td>
                  <td class="p-3"><span class="px-2 py-0.5 bg-blue-500/10 text-blue-400 text-xs rounded border border-blue-500/20">Empleado</span></td>
                  <td class="p-3"><span class="text-emerald-400">● Activo</span></td>
                  <td class="p-3 text-right"><button class="text-red-400 hover:text-red-300 text-xs">Revocar Acceso</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="bg-gray-950 p-6 rounded-xl border border-gray-800 flex flex-col">
          <h2 class="text-lg font-semibold text-gray-300 mb-4">Auditoría del Servidor</h2>
          <div class="space-y-3 flex-1 overflow-y-auto text-xs font-mono max-h-96">
            <div class="p-2.5 bg-gray-900 border-l-2 border-emerald-500 rounded-r">
              <span class="text-gray-500">[15:24:01]</span> <span class="text-emerald-400">AUTH_SUCCESS</span>: Sesión iniciada por usuario ID_481
            </div>
            <div class="p-2.5 bg-gray-900 border-l-2 border-blue-500 rounded-r">
              <span class="text-gray-500">[14:12:10]</span> <span class="text-blue-400">USER_CREATED</span>: Admin registró nuevo email corporativo
            </div>
            <div class="p-2.5 bg-gray-900 border-l-2 border-yellow-500 rounded-r">
              <span class="text-gray-500">[11:05:43]</span> <span class="text-yellow-400">AUTH_FAILED</span>: Intento fallido desde IP 192.168.1.55
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>