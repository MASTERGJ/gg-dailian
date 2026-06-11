#!/usr/bin/env python3
"""
gg代练 — 一键安装依赖
========================
Usage:
    python setup.py              # 安装所有依赖
    python setup.py --check      # 只检查不安装
    python setup.py --pip-only   # 只装pip包
    python setup.py --ffmpeg     # 只检查FFmpeg
"""

import os
import subprocess
import sys
import platform


def log(msg, status="INFO"):
    icons = {"INFO": "ℹ️", "OK": "✅", "FAIL": "❌", "SKIP": "⏭️", "WARN": "⚠️"}
    icon = icons.get(status, "ℹ️")
    print(f"  {icon} {msg}")


def run_cmd(cmd, timeout=60, check=False):
    """Run a command and return success/failure."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        output = "\n".join(
            part.strip() for part in (result.stdout, result.stderr) if part.strip()
        )
        return result.returncode == 0, output
    except FileNotFoundError:
        return False, "Command not found"
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def check_python():
    """Check Python version."""
    v = sys.version_info
    log(f"Python {v.major}.{v.minor}.{v.micro}", "OK")
    if v.major < 3 or (v.major == 3 and v.minor < 8):
        log(f"需要 Python 3.8+，当前是 {v.major}.{v.minor}", "FAIL")
        return False
    return True


def check_pip():
    """Check if pip is available."""
    ok, out = run_cmd([sys.executable, "-m", "pip", "--version"])
    if ok:
        log(f"pip: {out.split()[1]}", "OK")
        return True

    log("当前 Python 未找到 pip，尝试用 ensurepip 修复...", "WARN")
    bootstrapped, bootstrap_out = run_cmd(
        [sys.executable, "-m", "ensurepip", "--upgrade"], timeout=120
    )
    if bootstrapped:
        ok, out = run_cmd([sys.executable, "-m", "pip", "--version"])
        if ok:
            log(f"pip: {out.split()[1]}", "OK")
            return True

    _, path_pip = run_cmd(["pip", "--version"])
    if path_pip:
        log("PATH 中存在 pip，但不一定属于当前 Python 环境。", "WARN")
        log(path_pip.splitlines()[0], "INFO")

    detail = bootstrap_out or out
    if detail:
        log(f"pip 不可用原因: {detail.splitlines()[-1]}", "FAIL")
    else:
        log("pip 未找到", "FAIL")
    return False


def install_pip_packages(packages):
    """Install pip packages one by one."""
    success = True
    for pkg in packages:
        log(f"安装 {pkg}...", "INFO")
        ok, out = run_cmd(
            [sys.executable, "-m", "pip", "install", pkg],
            timeout=120
        )
        if ok:
            log(f"{pkg} 安装成功", "OK")
        else:
            log(f"{pkg} 安装失败: {out[-100:]}", "FAIL")
            success = False
    return success


def check_pip_packages():
    """Check which pip packages are installed."""
    packages = {
        "yt-dlp": "视频下载",
        "youtube-transcript-api": "YouTube字幕",
        "faster-whisper": "ASR语音识别",
        "Pillow": "图片合成",
    }
    all_ok = True
    missing = []

    for pkg, desc in packages.items():
        ok, out = run_cmd(
            [sys.executable, "-c", f"import {pkg.replace('-', '_')}; print('ok')"]
        )
        if ok:
            log(f"{pkg} ({desc}) 已安装", "OK")
        else:
            log(f"{pkg} ({desc}) 未安装", "WARN")
            missing.append(pkg)
            all_ok = False

    return all_ok, missing


def check_ffmpeg():
    """Check if FFmpeg is available."""
    ok, out = run_cmd(["ffmpeg", "-version"])
    if ok:
        version = out.split("\n")[0] if "\n" in out else out[:50]
        log(f"FFmpeg: {version}", "OK")
        return True
    else:
        log("FFmpeg 未找到", "WARN")
        log("请从 https://ffmpeg.org/download.html 安装", "INFO")
        log("或 winget install ffmpeg (Windows)", "INFO")
        return False


def install_ffmpeg_windows():
    """Try to install FFmpeg on Windows via winget."""
    if platform.system() != "Windows":
        log("非Windows系统，跳过winget安装", "SKIP")
        return False

    log("尝试通过 winget 安装 FFmpeg...", "INFO")
    ok, out = run_cmd(["winget", "install", "FFmpeg"], timeout=60)
    if ok:
        log("FFmpeg 安装成功", "OK")
        return True
    else:
        log("winget 安装失败，请手动安装 FFmpeg", "WARN")
        return False


def main():
    print("\n" + "=" * 56)
    print("  gg代练 — 一键环境检测与安装")
    print("=" * 56 + "\n")

    args = set(sys.argv[1:])
    check_only = "--check" in args
    pip_only = "--pip-only" in args
    ffmpeg_only = "--ffmpeg" in args

    # Step 1: Python
    if not ffmpeg_only:
        print("📋 [1/4] Python 环境")
        if not check_python():
            sys.exit(1)
        print()

    # Step 2: Pip
    if not ffmpeg_only:
        print("📋 [2/4] pip 包管理器")
        if not check_pip():
            sys.exit(1)
        print()

    # Step 3: Python dependencies
    if not ffmpeg_only:
        print("📋 [3/4] Python 依赖包")
        all_ok, missing = check_pip_packages()

        if missing and not check_only:
            print()
            log("正在安装缺失的包...", "INFO")
            if install_pip_packages(missing):
                print()
                log("所有依赖安装完成！", "OK")
            else:
                log("部分包安装失败，请手动安装：", "WARN")
                log(f"  pip install {' '.join(missing)}", "INFO")
        elif missing and check_only:
            log(f"缺少: {' '.join(missing)}。运行 setup.py 自动安装。", "WARN")
        else:
            log("所有依赖已就绪", "OK")
        print()

    # Step 4: FFmpeg
    if not pip_only:
        print("📋 [4/4] FFmpeg (系统工具)")
        has_ffmpeg = check_ffmpeg()
        if not has_ffmpeg and not check_only:
            install_ffmpeg_windows()
        print()

    # Summary
    print("=" * 56)
    if check_only:
        print("  检查完成。运行 python setup.py 自动安装缺失依赖。")
    else:
        print("  环境设置完成！现在可以运行 gg代练 了：")
        print()
        print(f"    {sys.executable} scripts/video_subtitle.py BV12ZDuBwEhX -R")
    print("=" * 56 + "\n")


if __name__ == "__main__":
    main()
