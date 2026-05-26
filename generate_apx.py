import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

# ============================================================
# ✏️  여기서 직접 수정하세요
# ============================================================
PROJECT_NAME = "Automatic"
BASE_PATH = r"C:\Users\Misun.Sim\Desktop\Misun\01. StackAnalyzer\workspace\SST-main"

# 함수명이 담긴 텍스트 파일 경로
FUNCTIONS_TXT_PATH = os.path.join(BASE_PATH, "function_list.txt")

# project 속성
PROJECT_VERSION = "25.04i"
PROJECT_BUILD   = "17783208"
PROJECT_TARGET  = "arm"          # 예: arm, x86 등

# executable .elf 경로
EXECUTABLE_PATH = r".\SST-main\sst_c\blinky.elf"

# ais / report 파일 경로
#AIS_PATH    = os.path.join(BASE_PATH, "global_annotations.ais")
REPORT_PATH = os.path.join(BASE_PATH, "report.txt")

# ARM 타겟 세부 정보 (PROJECT_TARGET == "arm" 일 때만 사용)
ARM_GENERAL_TARGET = "Cortex-M4"   # 예: Cortex-M4, Cortex-M7 등

# general_options
#PATH_REPLACEMENT = ""
#INCLUDE_PATH     = os.path.join(BASE_PATH, r"\SST-main\sst_c\src")

# 출력 파일 경로
OUTPUT_APX_PATH = os.path.join(BASE_PATH, f"{PROJECT_NAME}.apx")

# ============================================================


def parse_functions(filepath: str) -> list[str]:
    """텍스트 파일에서 함수명 목록을 읽어옵니다 (빈 줄 무시)."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return [line.strip() for line in lines if line.strip()]


def build_xml(functions: list[str]) -> ET.Element:
    """APX XML 트리를 생성합니다."""

    # ── project 루트 ──────────────────────────────────────────
    project = ET.Element("project", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:noNamespaceSchemaLocation": "http://www.absint.com/dtd/a3-apx-25.04i.xsd",
        "xmlns": "http://www.absint.com/apx",
        "version": PROJECT_VERSION,
        "build": PROJECT_BUILD,
        "target": PROJECT_TARGET,
    })

    # ── <files> ───────────────────────────────────────────────
    files = ET.SubElement(project, "files")

    executables = ET.SubElement(files, "executables")
    ET.SubElement(executables, "executable").text = EXECUTABLE_PATH

    #ET.SubElement(files, "ais").text    = AIS_PATH
    ET.SubElement(files, "report").text = REPORT_PATH

    # ── <options> ─────────────────────────────────────────────
    options = ET.SubElement(project, "options")

    analyses_options = ET.SubElement(options, "analyses_options")
    for tag, val in [
        ("interactive_pipeline_visualization", "true"),
        ("xml_variable_usage_statistics",      "true"),
        ("xml_object_size_statistics",         "true"),
        ("strip_compilation_path",             "true"),
    ]:
        ET.SubElement(analyses_options, tag).text = val

    # ARM 옵션 (target == arm 일 때만 추가)
    if PROJECT_TARGET.lower() == "arm":
        arm_options = ET.SubElement(options, "arm_options")
        general_arm = ET.SubElement(arm_options, "general")
        ET.SubElement(general_arm, "target").text = ARM_GENERAL_TARGET

    general_options = ET.SubElement(options, "general_options")
    #ET.SubElement(general_options, "path_replacement").text = PATH_REPLACEMENT
    #ET.SubElement(general_options, "include_path").text     = INCLUDE_PATH

    # ── <analyses> ────────────────────────────────────────────
    analyses = ET.SubElement(project, "analyses")

    
    # 함수별 stack_analysis / estimate_analysis
    for func in functions:

        # stack_analysis
        stack = ET.SubElement(analyses, "analysis", {
            "id":      f"{func}_stack",
            "type":    "stack_analysis",
            "enabled": "true",
            "group":   "stack_analysis",
        })
        ET.SubElement(stack, "analysis_start").text = func

        # estimate_analysis
        timing = ET.SubElement(analyses, "analysis", {
            "id":      f"{func}_timing",
            "type":    "estimate_analysis",
            "enabled": "true",
            "group":   "timing_profiler",
        })
        ET.SubElement(timing, "analysis_start").text = func

    return project


def prettify(element: ET.Element) -> str:
    """들여쓰기가 적용된 XML 문자열을 반환합니다."""
    raw = ET.tostring(element, encoding="unicode")
    parsed = minidom.parseString(raw)
    return parsed.toprettyxml(indent="  ")


def main():
    print(f"[1/3] 함수 목록 읽는 중: {FUNCTIONS_TXT_PATH}")
    functions = parse_functions(FUNCTIONS_TXT_PATH)
    print(f"      → {len(functions)}개 함수 발견: {functions}")

    print("[2/3] XML 생성 중...")
    root = build_xml(functions)

    print(f"[3/3] 파일 저장 중: {OUTPUT_APX_PATH}")
    xml_str = prettify(root)
    with open(OUTPUT_APX_PATH, "w", encoding="utf-8") as f:
        f.write(xml_str)

    print("✅ 완료!")


if __name__ == "__main__":
    main()
