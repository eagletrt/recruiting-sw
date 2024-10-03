#include "imgui/backends/imgui_impl_glfw.h"
#include "imgui/backends/imgui_impl_opengl2.h"
#include "imgui/imgui.h"
#include "implot/implot.h"
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

#include "app.h"

GLFWwindow *window;

GLFWwindow *open_window();
void init_imgui(GLFWwindow *window);
void render(GLFWwindow *window, const ImVec4 &clear_color);

void sig_handler(int sig_number) {
  if (sig_number == SIGINT || sig_number == SIGTERM) {
    glfwSetWindowShouldClose(window, 1);
  }
}

int main() {
  std::cout << "--- Project 1 ---\n" << std::endl;

  signal(SIGINT, sig_handler);
  signal(SIGTERM, sig_handler);

  std::cout << "Opening Window" << std::endl;
  window = open_window();
  init_imgui(window);
  ImGuiIO &io = ImGui::GetIO();
  ImVec4 clear_color = ImVec4(0.06f, 0.06f, 0.06f, 0.94f);
  std::cout << "Done" << std::endl;

  while (!glfwWindowShouldClose(window)) {
    glfwPollEvents();
    // Start the Dear ImGui frame
    ImGui_ImplOpenGL2_NewFrame();
    ImGui_ImplGlfw_NewFrame();
    ImGui::NewFrame();

    // renders tabs/buttons/...
    app_render();

    render(window, clear_color);
  }

  std::cout << "Shutdown" << std::endl;
  ImGui_ImplOpenGL2_Shutdown();
  ImGui_ImplGlfw_Shutdown();
  ImGui::DestroyContext();

  glfwDestroyWindow(window);
  glfwTerminate();

  return 0;
}

GLFWwindow *open_window() {
  // Setup window
  glewExperimental = GL_TRUE;
  if (!glfwInit())
    return nullptr;
  int x, y, w, h;
  glfwGetMonitorWorkarea(glfwGetPrimaryMonitor(), &x, &y, &w, &h);
  GLFWwindow *window = glfwCreateWindow(w, h, "Project 1", NULL, NULL);
  if (window == NULL)
    return nullptr;

  glfwMakeContextCurrent(window);
  glfwSwapInterval(1); // Enable vsync

  if (glewInit() != GLEW_OK)
    return nullptr;
  return window;
}

void init_imgui(GLFWwindow *window) {
  // Setup Dear ImGui context
  IMGUI_CHECKVERSION();
  ImGuiContext *ctx = ImGui::CreateContext();
  ImGuiIO &io = ImGui::GetIO();
  io.ConfigFlags |= ImGuiConfigFlags_DockingEnable; // Enable Docking
  io.ConfigViewportsNoDecoration = false;
  ImGuiStyle &style = ImGui::GetStyle();

  ImPlot::CreateContext();

  // Setup Platform/Renderer backends
  ImGui_ImplGlfw_InitForOpenGL(window, true);
  ImGui_ImplOpenGL2_Init();
}

void render(GLFWwindow *window, const ImVec4 &clear_color) {
  static int display_w, display_h;

  ImGui::Render();
  glfwGetFramebufferSize(window, &display_w, &display_h);

  glViewport(0, 0, display_w, display_h);
  glClearColor(clear_color.x * clear_color.w, clear_color.y * clear_color.w,
               clear_color.z * clear_color.w, clear_color.w);
  glClear(GL_COLOR_BUFFER_BIT);

  ImGui_ImplOpenGL2_RenderDrawData(ImGui::GetDrawData());
  if (ImGui::GetIO().ConfigFlags & ImGuiConfigFlags_ViewportsEnable) {
    GLFWwindow *backup_current_context = glfwGetCurrentContext();
    ImGui::UpdatePlatformWindows();
    ImGui::RenderPlatformWindowsDefault();
    glfwMakeContextCurrent(backup_current_context);
  } else {
    glfwMakeContextCurrent(window);
  }

  glfwSwapBuffers(window);
}
