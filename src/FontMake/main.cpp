/*
	TomoyoAfter PS2 字库制作程序

	Author:		kid

	Version:	

	History:
		2014.02.18	PS3 WHITE_ALBUM2 字库制作
		2008.10.31	原TomoyoAfter PS2 字库制作程序

*/

#define UNICODE
#include <windows.h>
#include <gdiplus.h>
//#include "resource.h"
#include <vector>
#include <fstream>
#include <vector>
#include <set>

#pragma comment(lib, "gdiplus.lib") 

using namespace std;
using namespace Gdiplus;

static vector<WCHAR> wa2_tbl;

bool ReadTBL_U(char* name)
{
	FILE* fp;
	fopen_s(&fp, name, "r, ccs=UTF-16LE");
	if (!fp) { return false; }

	int cnt = 0;
	wa2_tbl.clear();
	while (feof(fp) == 0)
	{
		wchar_t code = fgetwc(fp);
		//wstring t = code;
		wa2_tbl.push_back(code);
		++cnt;
	}
	fclose(fp);
	wprintf(L"Total %d char.\n", cnt);
	return true;
}

int GetEncoderClsid(const WCHAR* format, CLSID* pClsid)
{
   UINT  num = 0;          // number of image encoders
   UINT  size = 0;         // size of the image encoder array in bytes

   ImageCodecInfo* pImageCodecInfo = NULL;

   GetImageEncodersSize(&num, &size);
   if(size == 0)
      return -1;  // Failure

   pImageCodecInfo = (ImageCodecInfo*)(malloc(size));
   if(pImageCodecInfo == NULL)
      return -1;  // Failure

   GetImageEncoders(num, size, pImageCodecInfo);

   for(UINT j = 0; j < num; ++j)
   {
      if( wcscmp(pImageCodecInfo[j].MimeType, format) == 0 )
      {
         *pClsid = pImageCodecInfo[j].Clsid;
         free(pImageCodecInfo);
         return j;  // Success
      }    
   }

   free(pImageCodecInfo);
   return -1;  // Failure
}

void Paint_WA2(WCHAR* fontname, WCHAR* filename, const int TextureWidth, const int TextureHeight, const int FontBlockWidth, const int FontBlockHeight, const Gdiplus::REAL FontSize)
{
	SolidBrush  solidBrush2(Color(255, 255, 255, 255));
	SolidBrush  solidBrush3(Color(0xf0, 0, 0, 0));

	FontFamily  fontFamily1(fontname);
	Font        font1(&fontFamily1, FontSize, FontStyleBold, UnitPixel);

	FontFamily  fontFamilyAscii(L"Arial Narrow");
	Font        fontAscii(&fontFamilyAscii, FontSize, FontStyleRegular, UnitPixel);


	int num = 0;
	vector<WCHAR>::const_iterator it = wa2_tbl.begin();
	Bitmap bitmap1(TextureWidth, TextureHeight);
	Graphics g1(&bitmap1);
	g1.FillRectangle(&solidBrush3, 0, 0, TextureWidth, TextureHeight);
	g1.SetTextRenderingHint(TextRenderingHintAntiAlias);
	wprintf(L"begin\n");

	{
		float x = 0.0f;
		float y = 0.0f;
		for (int i = 0; i < TextureHeight / FontBlockHeight && it != wa2_tbl.end(); ++i)
		{
			for (int j = 0; j < TextureWidth / FontBlockWidth && it != wa2_tbl.end(); ++j, ++it, x += FontBlockWidth)
			{
				wstring t(&(*it), 1);
				if (*it <= L'}') { wprintf(L"draw ascii\n"); g1.DrawString(t.c_str(), -1, &fontAscii, PointF(x, y), &solidBrush2); }
				else { g1.DrawString(t.c_str(), -1, &font1, PointF(x, y), &solidBrush2); }
			}
			y += FontBlockHeight;
			x = 0.0f;
		}

	} 
	if (it != wa2_tbl.end()) { wprintf(L"Make Font error. %d ok\n", it - wa2_tbl.begin()); return; }
	CLSID pngClsid;
	GetEncoderClsid(L"image/png", &pngClsid);
	bitmap1.Save(filename, &pngClsid);
	wprintf(L"Make font %s ...\n", filename);
}

void MakeFont_WA2(char* name1, char* name2)
{
	if (!ReadTBL_U(name1))
	{
		_wperror(L"Read TBL file error ");
		return ;
	}

	GdiplusStartupInput gdiplusStartupInput;
	ULONG_PTR           gdiplusToken;

	// Initialize GDI+.
	GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
	Paint_WA2(L"方正准圆_GBK", L"font1.png", 2040, 2160, 40, 40, 28);

	if (!ReadTBL_U(name2))
	{
		_wperror(L"Read TBL file error ");
		return;
	}

	//wa2_tbl.erase(wa2_tbl.begin() + 4, wa2_tbl.begin() + 6);	//	"()"
	Paint_WA2(L"方正准圆_GBK", L"font3.png", 2048, 352, 16, 16, 14);
	GdiplusShutdown(gdiplusToken);
}

int main(int argc, char* argv[])
{
	if (argc < 2)
	{
		wprintf(L"Error argu.\n");
		return -1;
	}

	if (!strcmp(argv[1], "-fwa2"))
	{
		MakeFont_WA2(argv[2], argv[3]);
	}

	return 0;
}

