#include "app.h"

#include "implot/implot.h"

void app_render() {

  ImGui::ShowDemoWindow();
  ImPlot::ShowDemoWindow();
  ImGui::Begin("Project 1");
  ImGui::Text("Project 1");

  ImGui::End();
}
